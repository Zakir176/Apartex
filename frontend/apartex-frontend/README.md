# Apartex Frontend

Vue.js 3 frontend application for the Apartex apartment booking platform.

## 🚀 Getting Started

### Prerequisites

- Node.js 16 or higher
- npm or yarn package manager

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:8080` (or the port specified by Vite)

3. **Build for production**:
   ```bash
   npm run build
   ```

4. **Preview production build**:
   ```bash
   npm run preview
   ```

## 🏗️ Project Structure

```
apartex-frontend/
├── src/
│   ├── api/                    # API client functions
│   │   ├── index.js           # API configuration
│   │   ├── auth.js             # Authentication API
│   │   ├── apartments.js       # Apartments API
│   │   ├── bookings.js         # Bookings API
│   │   ├── dashboard.js        # Dashboard API
│   │   ├── loyalty.js          # Loyalty API
│   │   └── uploads.js          # Uploads API
│   ├── components/             # Vue components
│   │   ├── apartments/        # Apartment-related components
│   │   │   ├── ApartmentList.vue
│   │   │   └── SearchBar.vue
│   │   ├── common/            # Common/shared components
│   │   │   ├── NavBar.vue
│   │   │   └── AppFooter.vue
│   │   ├── dashboard/         # Dashboard components
│   │   │   ├── ApartmentManager.vue
│   │   │   ├── OwnerStatsCard.vue
│   │   │   ├── PayoutHistoryTable.vue
│   │   │   └── RevenueChart.vue
│   │   ├── ApartmentCard.vue
│   │   ├── BookingForm.vue
│   │   └── DebugState.vue
│   ├── router/
│   │   └── index.js           # Vue Router configuration
│   ├── services/              # Service layer
│   │   ├── api.js             # Base API service
│   │   ├── auth.js            # Authentication service
│   │   ├── apartments.js      # Apartment service
│   │   ├── bookings.js        # Booking service
│   │   └── loyalty.js         # Loyalty service
│   ├── stores/                # Pinia state management
│   │   ├── index.js           # Store configuration
│   │   ├── auth.js            # Authentication store
│   │   ├── apartments.js     # Apartments store
│   │   ├── bookings.js        # Bookings store
│   │   ├── dashboard.js       # Dashboard store
│   │   ├── loyalty.js         # Loyalty store
│   │   └── theme.js           # Theme store
│   ├── utils/                 # Utility functions
│   │   ├── errorHandler.js    # Error handling utilities
│   │   └── toast.js           # Toast notification utilities
│   ├── views/                 # Page views
│   │   ├── HomeView.vue       # Home page
│   │   ├── ApartmentsView.vue # Apartments listing
│   │   ├── ApartmentDetailView.vue
│   │   ├── BookingsView.vue
│   │   ├── DashboardView.vue  # Owner dashboard
│   │   ├── LoyaltyView.vue
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── OwnerLoginView.vue
│   │   ├── OwnerRegisterView.vue
│   │   ├── OwnerHomeView.vue
│   │   ├── OwnerApartmentsView.vue
│   │   ├── OwnerBookingsView.vue
│   │   ├── OwnerPayoutsView.vue
│   │   ├── ProfileView.vue
│   │   ├── WishlistView.vue
│   │   ├── TestView.vue
│   │   └── NotFoundView.vue
│   ├── App.vue                # Root component
│   └── main.js                # Application entry point
├── index.html                 # HTML template
├── package.json               # Dependencies and scripts
└── vite.config.js            # Vite configuration
```

## 🛠️ Tech Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management library
- **PrimeVue** - UI component library
- **Axios** - HTTP client for API requests
- **date-fns** - Date utility library
- **Sass** - CSS preprocessor

## 📱 Features

### Guest Features
- 🔍 Search and filter apartments
- 📅 View apartment details and availability
- 🏠 Book apartments
- 💎 View and redeem loyalty rewards
- 👤 User profile management
- ❤️ Wishlist functionality

### Owner Features
- 🏠 Manage apartment listings
- 📊 Dashboard with analytics
- 💰 View payout history
- 📈 Revenue charts and statistics
- 📅 Manage bookings
- 🖼️ Upload apartment images

## 🔌 API Configuration

The frontend communicates with the backend API. Configure the API base URL in `src/api/index.js` or through environment variables.

Default API endpoint: `http://localhost:8000`

## 🎨 Styling

The application uses:
- **PrimeVue** components for UI elements
- **Sass** for custom styling
- **Inter** font family (Google Fonts)

## 🔐 Authentication

Authentication is handled through:
- JWT tokens stored in localStorage
- Axios interceptors for automatic token injection
- Pinia store for authentication state management

## 📦 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run serve` - Serve with vue-cli-service (legacy)

## 🏗️ State Management

State is managed using Pinia stores:
- **auth** - User authentication state
- **apartments** - Apartment listings and filters
- **bookings** - User bookings
- **dashboard** - Owner dashboard data
- **loyalty** - Loyalty points and rewards
- **theme** - Application theme settings

## 🛣️ Routing

Routes are configured in `src/router/index.js`. The application includes:

- Public routes: Home, Apartments, Login, Register
- Protected routes: Bookings, Profile, Wishlist, Loyalty
- Owner routes: Dashboard, Owner Apartments, Owner Bookings, Payouts

## 🔧 Configuration

### Vite Configuration

Vite configuration is in `vite.config.js`. It includes:
- Vue plugin configuration
- Development server settings
- Build options

### Environment Variables

Create a `.env` file for environment-specific variables:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Access in code via `import.meta.env.VITE_API_BASE_URL`

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

### Deploy to Vercel

The application is configured for Vercel deployment. The frontend is available at `https://apartex.vercel.app`.

### Static Hosting

You can deploy the `dist/` folder to any static hosting service:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Any other static hosting provider

## 🐛 Debugging

- Use Vue DevTools browser extension
- Check browser console for errors
- Use the DebugState component for state inspection
- Check network tab for API requests

## 📝 Code Style

- Follow Vue 3 Composition API best practices
- Use Pinia for state management
- Keep components focused and reusable
- Use TypeScript-style JSDoc comments where helpful

## 🔄 Development Workflow

1. Make changes to components/services
2. Hot module replacement (HMR) will update automatically
3. Test in browser
4. Check console for errors
5. Build and test production build before deploying

## 📄 License

MIT License - see the main [LICENSE](../../LICENSE) file for details.

## 🔗 Related Documentation

- [Vue.js Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [PrimeVue Documentation](https://primevue.org/)
- [Vue Router Documentation](https://router.vuejs.org/)
