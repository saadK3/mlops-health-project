# Health Monitoring Dashboard - Frontend

A modern, responsive React-based dashboard for health monitoring and disease outbreak tracking. Built with React, Vite, TailwindCSS, and interactive data visualization libraries.

## Features

- **Landing Page**: Overview of the health monitoring system
- **Citizen Dashboard**: Public-facing dashboard for citizens to view health data and outbreak information
- **Authority Dashboard**: Administrative dashboard for health authorities with advanced analytics
- **Interactive Maps**: Leaflet-based maps for geographical outbreak visualization
- **Data Visualization**: Charts and graphs using Recharts library
- **Responsive Design**: Mobile-friendly interface with TailwindCSS

## Tech Stack

- **Framework**: React 19.2
- **Build Tool**: Vite 7.2
- **Styling**: TailwindCSS 3.4
- **Routing**: React Router DOM 7.9
- **HTTP Client**: Axios 1.13
- **Maps**: Leaflet 1.9 + React Leaflet 5.0
- **Charts**: Recharts 3.4
- **Icons**: Lucide React 0.554

## Prerequisites

Before running the frontend, ensure you have:

- **Node.js** (v18 or higher recommended)
- **npm** (comes with Node.js)

## Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

## Running the Application

### Development Mode

Start the development server with hot module replacement (HMR):

```bash
npm run dev
```

The application will be available at `http://localhost:5173` (default Vite port).

### Production Build

To create a production-optimized build:

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

To preview the production build locally:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── pages/           # Page components
│   │   ├── Landing.jsx
│   │   ├── CitizenDashboard.jsx
│   │   └── AuthorityDashboard.jsx
│   ├── App.jsx          # Main app component with routing
│   └── main.jsx         # Application entry point
├── public/              # Static assets
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
└── tailwind.config.js   # TailwindCSS configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint for code quality

## Backend Integration

The frontend connects to the Flask backend API. Make sure the backend is running on `http://localhost:5000` (or update the API endpoint in the code accordingly).

## Development Notes

- The app uses React Router for client-side routing
- TailwindCSS is configured with custom colors and utilities
- Leaflet maps require proper CSS imports for correct rendering
- All API calls are made using Axios

## Troubleshooting

### Port Already in Use
If port 5173 is already in use, Vite will automatically try the next available port.

### Map Not Displaying
Ensure Leaflet CSS is properly imported in your component or main CSS file.

### API Connection Issues
Verify that the backend server is running and accessible at the configured endpoint.
