from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models.booking import Booking
from app.models.apartment import Property
from app.models.payout import Payout

class DashboardService:
    
    @staticmethod
    def get_revenue_summary(owner_id: int, db: Session):
        """Get revenue summary for owner dashboard."""
        # Total revenue from completed bookings
        total_revenue = db.query(func.sum(Booking.total_price)).join(Property).filter(
            Property.owner_id == owner_id,
            Booking.status == "completed"
        ).scalar() or 0
        
        # Monthly revenue (current month)
        current_month = datetime.now().replace(day=1)
        monthly_revenue = db.query(func.sum(Booking.total_price)).join(Property).filter(
            Property.owner_id == owner_id,
            Booking.status == "completed",
            Booking.created_at >= current_month
        ).scalar() or 0
        
        # Pending payouts (revenue from confirmed bookings not yet paid out)
        pending_payouts = db.query(func.sum(Booking.total_price)).join(Property).filter(
            Property.owner_id == owner_id,
            Booking.status == "confirmed"
        ).scalar() or 0
        
        # Occupancy rate (percentage of days booked)
        total_days = 30  # Assuming 30-day period for simplicity
        booked_days = db.query(Booking).join(Property).filter(
            Property.owner_id == owner_id,
            Booking.status.in_(["confirmed", "completed"]),
            Booking.check_in >= datetime.now() - timedelta(days=30)
        ).count()
        
        occupancy_rate = (booked_days / total_days) * 100 if total_days > 0 else 0
        
        # Average Daily Rate (ADR)
        total_bookings = db.query(Booking).join(Property).filter(
            Property.owner_id == owner_id,
            Booking.status.in_(["confirmed", "completed"])
        ).count()
        
        adr = float(total_revenue / total_bookings) if total_bookings > 0 else 0.0
        revpar = float(adr * (occupancy_rate / 100.0))
        
        return {
            "total_revenue": float(total_revenue),
            "monthly_revenue": float(monthly_revenue),
            "pending_payouts": float(pending_payouts),
            "occupancy_rate": round(occupancy_rate, 2),
            "average_daily_rate": round(adr, 2),
            "revpar": round(revpar, 2)
        }
    
    @staticmethod
    def get_booking_trends(owner_id: int, db: Session, months: int = 6):
        """Get booking trends for the last N months."""
        trends = []
        
        for i in range(months):
            month_date = datetime.now().replace(day=1) - timedelta(days=30*i)
            month_str = month_date.strftime("%Y-%m")
            
            # Count bookings and revenue for this month
            month_bookings = db.query(Booking).join(Property).filter(
                Property.owner_id == owner_id,
                extract('year', Booking.created_at) == month_date.year,
                extract('month', Booking.created_at) == month_date.month
            ).count()
            
            month_revenue = db.query(func.sum(Booking.total_price)).join(Property).filter(
                Property.owner_id == owner_id,
                extract('year', Booking.created_at) == month_date.year,
                extract('month', Booking.created_at) == month_date.month
            ).scalar() or 0

            month_occ = round((month_bookings / 30.0) * 100.0, 2)
            month_adr = (float(month_revenue) / month_bookings) if month_bookings > 0 else 0.0
            month_revpar = round(month_adr * (month_occ / 100.0), 2)
            
            trends.append({
                "period": month_str,
                "bookings": month_bookings,
                "revenue": float(month_revenue),
                "occupancy_rate": month_occ,
                "revpar": month_revpar
            })
        
        return list(reversed(trends))  # Return in chronological order
    
    @staticmethod
    def get_recent_bookings(owner_id: int, db: Session, limit: int = 10):
        """Get recent bookings for owner's apartments."""
        bookings = db.query(Booking).join(Property).filter(
            Property.owner_id == owner_id
        ).order_by(Booking.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": booking.id,
                "apartment_title": booking.property.title if booking.property else "",
                "check_in": booking.check_in,
                "check_out": booking.check_out,
                "total_price": float(booking.total_price),
                "status": booking.status,
                "created_at": booking.created_at
            }
            for booking in bookings
        ]
    
    @staticmethod
    def get_top_performing_apartments(owner_id: int, db: Session, limit: int = 5):
        """Get top performing apartments by revenue."""
        apartments = db.query(Property).filter(
            Property.owner_id == owner_id
        ).all()
        
        performance_data = []
        
        for apartment in apartments:
            total_revenue = db.query(func.sum(Booking.total_price)).filter(
                Booking.property_id == apartment.id,
                Booking.status.in_(["confirmed", "completed"])
            ).scalar() or 0
            
            booking_count = db.query(Booking).filter(
                Booking.property_id == apartment.id,
                Booking.status.in_(["confirmed", "completed"])
            ).count()
            
            performance_data.append({
                "id": apartment.id,
                "title": apartment.title,
                "total_revenue": float(total_revenue),
                "booking_count": booking_count,
                "occupancy_rate": round((booking_count / 30) * 100, 2)  # Simplified
            })
        
        return sorted(performance_data, key=lambda x: x["total_revenue"], reverse=True)[:limit]
