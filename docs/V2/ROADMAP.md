# 🗺️ Apartex Product Roadmap

This roadmap outlines the future direction of the Apartex platform. Our goal is to evolve from a premium booking engine into a comprehensive hospitality ecosystem.

---

## 🟢 Phase 1: Foundation (Current)
*Focus on core booking functionality and owner tools.*

- [x] **Core API**: Robust FastAPI backend with JWT authentication.
- [x] **Apartment Management**: CRUD operations for property owners.
- [x] **Booking Engine**: Real-time availability and reservation logic.
- [x] **Loyalty System**: Basic points earning and reward redemption.
- [x] **Owner Dashboard**: Revenue tracking and payout history.
- [x] **Responsive UI**: Glassmorphism design with Vue 3.

---

## 🟡 Phase 2: Multi-Property Expansion + Walk-in Booking (v2 — September 2026)
*Expanding from apartments-only to all accommodation types, and adding offline-first booking support.*

- [ ] **🏨 Multi-property type support**: Hotels, lodges, and guest houses alongside apartments
- [ ] **🛏️ Room model**: Hotels have multiple bookable room types per property (Standard, Deluxe, Suite etc.)
- [ ] **🚶 Walk-in Booking (POS mode)**: Owners record physical guest arrivals without requiring a guest account — name, phone, dates, payment method (Cash / Mobile Money / Card). Confirmation card shareable via WhatsApp
- [ ] **🏷️ Property type filters**: Browse by Apartment / Hotel / Lodge / Guest House
- [ ] **🔄 Alembic migrations**: Proper DB migration management replacing manual ALTER TABLE
- [ ] **🐘 PostgreSQL**: Production-grade database replacing SQLite

---

## 🟠 Phase 3: Revenue & Connectivity (Future)
*Payment processing, notifications, and platform reach.*

- [ ] **💳 Payment Integration**: Mobile money (MTN/Airtel Zambia) + card payments
- [ ] **📧 Notification System**: WhatsApp/SMS booking confirmations (more relevant than email in Zambia)
- [ ] **💬 Real-time Messaging**: In-app chat between guests and property owners
- [ ] **⭐ Advanced Reviews**: Image uploads in reviews and verified stay badges
- [ ] **🔐 Social Login**: Google and phone number login

---

## 🔴 Phase 4: Ecosystem Expansion (Long-term)
*Broadening the horizons of Apartex.*

- [ ] **📱 Native Mobile Apps**: High-performance iOS and Android applications.
- [ ] **🤝 Affiliate Program**: Referral system for guests and influencers.
- [ ] **🛍️ Experiences Marketplace**: Booking tours and activities alongside apartments.
- [ ] **🔌 Developer API**: Public API for third-party integrations.

---

## 🛠️ Technical Debt & Quality Goals
- **Unit Testing**: Increase coverage to >80% for both frontend and backend.
- **CI/CD**: Automate testing and deployment pipelines.
- **Performance**: Optimize image loading and database queries.
- **Accessibility**: Ensure WCAG 2.1 compliance across the frontend.

---

*Note: This roadmap is a living document and will be updated as we progress and gather user feedback.*
