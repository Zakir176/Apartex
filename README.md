# 🏨 Apartex

**Apartex** is a premium apartment booking ecosystem designed to bridge the gap between luxury property owners and globetrotting guests. Built with a high-performance FastAPI backend and a reactive Vue.js 3 frontend, it offers a seamless experience for both property management and vacation discovery.

---

## ✨ Project Showcase

### 🌟 Public Landing Page
![Apartex Animated Public Landing Page Hero](docs/screenshots/hero.png)
*State-of-the-art public landing page featuring animated mesh gradients, live trust counters, and zero-markup guarantees.*

<div align="center">
  <img src="docs/screenshots/landing_features.png" width="48%" />
  <img src="docs/screenshots/home_app.png" width="48%" />
</div>

*Left: Platform value pillars & comparison matrix ("Why Apartex"). Right: Interactive guest stay search & discovery engine.*

<div align="center">
  <img src="docs/screenshots/loyalty.png" width="48%" />
  <img src="docs/screenshots/dashboard.png" width="48%" />
</div>

*Left: Apartex VIP Club rewards & tier benefits dashboard. Right: Comprehensive host revenue & occupancy analytics dashboard.*

---

## 🚀 Vision & Key Features

### 💎 For Guests
- **🔍 Smart Search**: Find the perfect stay using advanced filtering and location-based discovery.
- **📅 Real-time Booking**: Instant confirmation with checking-in/out date validation.
- **🏆 Loyalty Rewards**: Earn points on every stay to unlock exclusive tiers and rewards.
- **💖 Wishlist**: Curate your dream vacation list with a single click.

### 📊 For Property Owners
- **🏠 Listing Management**: Create and manage detailed property profiles with image support.
- **📈 Advanced Analytics**: Track revenue, occupancy rates, and booking trends at a glance.
- **💰 Payout Tracking**: Transparent history of earnings and payout statuses.
- **🛡️ Secure Access**: Role-based authentication ensuring data privacy.

---

## 🛠️ Tech Stack & Architecture

### Backend (FastAPI)
- **FastAPI**: Asynchronous Python framework for high-throughput APIs.
- **SQLAlchemy 2.0**: Modern ORM for flexible database modeling.
- **JWT Auth**: Secure token-based authentication with refresh cycles.
- **Pydantic**: Robust data validation and serialization.

### Frontend (Vue 3)
- **Vue.js 3 + Vite**: Lightning-fast development and optimized build pipeline.
- **Pinia**: Centralized state management for complex reactive data.
- **PrimeVue**: High-quality UI component library.
- **Vanilla CSS**: Bespoke premium styling with glassmorphism and smooth transitions.

---

## 📈 Project Health & Development
We maintain high standards for code quality and security. For a detailed breakdown of system design, technical debt, and our vision, please refer to:

- 🏗️ **[Architecture Overview](./docs/ARCHITECTURE.md)** - Deep dive into tech stack and data flow.
- 🗄️ **[Database Schema](./docs/DATABASE.md)** - Visual and technical breakdown of the data model.
- 🗺️ **[Project Roadmap](./docs/ROADMAP.md)** - Our vision for future phases.
- 🤝 **[Contributing Guide](./CONTRIBUTING.md)** - How to get involved with the project.

---

## 🏗️ Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **SQLite** (Default) or PostgreSQL

### Quick Setup

1. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend/apartex-frontend
   npm install
   npm run dev
   ```

---

## 🤝 Contributing & License
Contributions are welcome! Please feel free to submit a Pull Request.  
Distributed under the **MIT License**. Created by **Zakir Motala**.


