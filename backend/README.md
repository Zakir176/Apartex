# Apartex Backend

FastAPI-based backend API for the Apartex apartment booking platform.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (optional, SQLite is used by default)

### Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=sqlite:///./apartex.db
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   BCRYPT_ROUNDS=12
   ```
   
   For PostgreSQL:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/apartex
   ```

4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```
   
   Or with custom host/port:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **API Root**: `http://localhost:8000/`

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py          # Application settings
│   │   └── security.py         # Password hashing, JWT utilities
│   ├── database.py             # Database connection and session
│   ├── models/
│   │   ├── user.py             # User model
│   │   ├── apartment.py        # Apartment model
│   │   ├── booking.py          # Booking model
│   │   ├── loyalty.py          # Loyalty/Reward model
│   │   └── payout.py           # Payout model
│   ├── routers/
│   │   ├── auth.py             # Basic authentication
│   │   ├── auth_enhanced.py    # Enhanced authentication with refresh tokens
│   │   ├── apartments.py       # Apartment CRUD operations
│   │   ├── bookings.py         # Booking management
│   │   ├── loyalty.py          # Loyalty program endpoints
│   │   ├── dashboard.py        # Owner dashboard analytics
│   │   └── uploads.py          # File upload handling
│   ├── schemas/
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── apartment.py        # Apartment schemas
│   │   ├── booking.py          # Booking schemas
│   │   ├── loyalty.py          # Loyalty schemas
│   │   ├── dashboard.py        # Dashboard schemas
│   │   └── token.py            # Token schemas
│   ├── services/
│   │   ├── dashboard_service.py # Dashboard business logic
│   │   └── loyalty_service.py  # Loyalty program logic
│   └── scripts/
│       └── seed_demo_data.py   # Database seeding script
├── tests/                      # Test files
├── uploads/                     # Uploaded files directory
├── main.py                      # FastAPI application entry point
└── requirements.txt             # Python dependencies
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `POST /auth-enhanced/register` - Enhanced registration
- `POST /auth-enhanced/login` - Enhanced login with refresh token
- `POST /auth-enhanced/refresh` - Refresh access token

### Apartments
- `GET /apartments` - List all apartments (with filters)
- `GET /apartments/{id}` - Get apartment details
- `POST /apartments` - Create new apartment (owner only)
- `PUT /apartments/{id}` - Update apartment (owner only)
- `DELETE /apartments/{id}` - Delete apartment (owner only)
- `GET /apartments/availability/{id}` - Check apartment availability

### Bookings
- `GET /bookings` - Get user's bookings
- `POST /bookings` - Create a new booking
- `GET /bookings/{id}` - Get booking details
- `PUT /bookings/{id}/cancel` - Cancel a booking

### Loyalty
- `GET /loyalty/rewards` - Get user's loyalty rewards
- `GET /loyalty/points` - Get user's loyalty points
- `POST /loyalty/redeem` - Redeem a reward

### Dashboard (Owner Only)
- `GET /dashboard/stats` - Get owner statistics
- `GET /dashboard/revenue` - Get revenue analytics
- `GET /dashboard/payouts` - Get payout history

### Uploads
- `POST /upload/image` - Upload an image (authenticated users)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## 🗄️ Database

The application uses SQLAlchemy ORM and supports:
- **SQLite** (default) - For development
- **PostgreSQL** - For production (configure via `DATABASE_URL`)

Database tables are automatically created on startup via `Base.metadata.create_all()`.

### Database Models

- **User** - User accounts (guests and owners)
- **Apartment** - Property listings
- **Booking** - Reservation records
- **LoyaltyReward** - Loyalty program rewards
- **Payout** - Owner payout records

## 🧪 Testing

Test files are located in the `tests/` directory. Run tests using pytest or your preferred testing framework.

Example test files:
- `test_auth.py` - Authentication tests
- `test_loyalty.py` - Loyalty program tests
- `test_availability_fix.py` - Availability checking tests

## 📦 Dependencies

Key dependencies:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **pydantic** - Data validation
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **bcrypt** - Password hashing algorithm
- **python-multipart** - File uploads
- **psycopg2-binary** - PostgreSQL adapter

See `requirements.txt` for the complete list.

## 🔧 Configuration

Configuration is managed through:
1. Environment variables (`.env` file)
2. `app/core/config.py` - Settings class with defaults

### Environment Variables

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key (change in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration (default: 30)
- `BCRYPT_ROUNDS` - Password hashing rounds (default: 12)

## 🚀 Deployment

### Production Considerations

1. **Change SECRET_KEY** - Use a strong, random secret key
2. **Use PostgreSQL** - Switch from SQLite to PostgreSQL
3. **Set up CORS** - Update allowed origins in `main.py`
4. **Environment variables** - Use secure environment variable management
5. **Static files** - Configure proper static file serving
6. **HTTPS** - Use HTTPS in production

### Running with Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Seeding Demo Data

To seed the database with demo data:

```bash
python -m app.scripts.seed_demo_data
```

## 🐛 Debugging

- Check logs in the console output
- Use FastAPI's interactive API docs at `/docs`
- Enable debug mode with `--reload` flag in uvicorn

## 📄 License

MIT License - see the main [LICENSE](../LICENSE) file for details.


