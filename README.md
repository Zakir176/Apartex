# Apartex

Apartex is a modern apartment booking platform that connects property owners with guests. The platform enables owners to list their apartments, manage bookings, track revenue, and receive payouts, while guests can search, book apartments, and earn loyalty rewards.

## 🏗️ Project Structure

```
Apartex/
├── backend/              # FastAPI backend application
│   ├── app/             # Main application code
│   │   ├── core/        # Core configuration and security
│   │   ├── models/      # SQLAlchemy database models
│   │   ├── routers/     # API route handlers
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic services
│   │   └── scripts/     # Utility scripts (seed data, etc.)
│   ├── tests/           # Test files
│   ├── uploads/         # Uploaded files directory
│   ├── main.py          # FastAPI application entry point
│   └── requirements.txt # Python dependencies
│
├── frontend/
│   └── apartex-frontend/  # Vue.js frontend application
│       ├── src/
│       │   ├── api/        # API client functions
│       │   ├── components/ # Vue components
│       │   ├── router/     # Vue Router configuration
│       │   ├── services/   # Service layer
│       │   ├── stores/     # Pinia state management
│       │   ├── utils/      # Utility functions
│       │   └── views/      # Page views
│       ├── package.json    # Node.js dependencies
│       └── vite.config.js  # Vite configuration
│
└── LICENSE               # MIT License
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for frontend)
- **PostgreSQL** (optional, SQLite is used by default)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory (optional):
   ```env
   DATABASE_URL=sqlite:///./apartex.db
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/apartex-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:8080` (or the port specified by Vite)

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management for Vue
- **PrimeVue** - UI component library
- **Axios** - HTTP client
- **date-fns** - Date utility library

## 📋 Features

### For Guests
- 🔍 Search and browse apartments
- 📅 Book apartments with date selection
- 💎 Loyalty rewards program
- 👤 User profiles and wishlists
- 📱 Responsive design

### For Property Owners
- 🏠 Manage apartment listings
- 📊 Dashboard with revenue analytics
- 💰 Payout history and management
- 📈 Booking statistics
- 🖼️ Image uploads for apartments

## 🔐 Authentication

The application supports two types of users:
- **Guests** - Can browse and book apartments
- **Owners** - Can manage properties and view analytics

Authentication is handled via JWT tokens with secure password hashing using bcrypt.

## 📚 API Documentation

Once the backend server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing

Backend tests are located in the `backend/tests/` directory. Run tests using your preferred Python testing framework.

## 📝 Environment Variables

### Backend (.env)
- `DATABASE_URL` - Database connection string (default: SQLite)
- `SECRET_KEY` - Secret key for JWT token signing
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Zakir Motala**

---

For more detailed information, please refer to:
- [Backend README](backend/README.md)
- [Frontend README](frontend/apartex-frontend/README.md)

