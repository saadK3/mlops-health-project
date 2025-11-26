# MLOps Health Monitoring Project

A comprehensive health monitoring and disease outbreak tracking system built with machine learning, federated learning, and modern web technologies. This project combines a Flask-based backend with MLflow integration and a React-based frontend dashboard.

## 🎯 Project Overview

This MLOps project provides:
- **Disease Outbreak Prediction**: ML models for predicting health trends
- **Federated Learning**: Distributed training across multiple clients
- **Data Drift Detection**: Monitoring for data quality and model performance
- **Interactive Dashboards**: Citizen and authority-facing web interfaces
- **MLflow Integration**: Experiment tracking and model management
- **Real-time Monitoring**: Health metrics and outbreak visualization

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Features](#features)
- [Documentation](#documentation)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

### Backend Requirements
- **Python** 3.8 or higher
- **pip** (Python package manager)

### Frontend Requirements
- **Node.js** v18 or higher
- **npm** (comes with Node.js)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd mlops-health-project
```

### 2. Backend Setup

#### Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
cd ..
```

## 🚀 Running the Application

You'll need to run both the backend and frontend servers.

### Option 1: Run in Separate Terminals

#### Terminal 1 - Backend Server

```bash
# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Run the Flask backend
python app.py
```

The backend API will be available at `http://localhost:5000`

#### Terminal 2 - Frontend Development Server

```bash
# Navigate to frontend directory
cd frontend

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Option 2: Quick Start Script

You can create a simple script to run both servers (example for Windows):

**`start.bat`:**
```batch
@echo off
start cmd /k "venv\Scripts\activate && python app.py"
start cmd /k "cd frontend && npm run dev"
```

## 📁 Project Structure

```
mlops-health-project/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── pages/           # Dashboard pages
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── README.md            # Frontend-specific documentation
│
├── data/                    # Data files
│   └── MLOPs_data.csv      # Health monitoring dataset
│
├── model/                   # Trained models (gitignored)
├── mlruns/                  # MLflow experiment tracking (gitignored)
├── notebooks/               # Jupyter notebooks for analysis
│
├── app.py                   # Main Flask API server
├── train.py                 # Model training script
├── train_simple.py          # Simplified training script
├── data_drift.py            # Data drift detection
├── run_distributed_fl.py    # Federated learning orchestration
├── server.py                # Flower federated learning server
├── client.py                # Flower federated learning client
├── test_app.py              # API tests
├── test_model_performance.py # Model evaluation
│
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── deployment.yaml         # Kubernetes deployment config
├── .gitignore
└── README.md               # This file
```

## ✨ Features

### Backend (Flask + MLflow)
- RESTful API for health data
- Machine learning model serving
- Federated learning support with Flower
- Data drift detection and monitoring
- MLflow experiment tracking
- Model versioning and registry

### Frontend (React + Vite)
- **Landing Page**: System overview and navigation
- **Citizen Dashboard**: Public health information and outbreak maps
- **Authority Dashboard**: Advanced analytics and administrative tools
- Interactive data visualizations with Recharts
- Geographical outbreak mapping with Leaflet
- Responsive design with TailwindCSS

## 📚 Documentation

Additional documentation files:
- [`MLFLOW_GUIDE.md`](MLFLOW_GUIDE.md) - MLflow setup and usage
- [`MLFLOW_INTEGRATION_SUMMARY.md`](MLFLOW_INTEGRATION_SUMMARY.md) - Integration details
- [`frontend/README.md`](frontend/README.md) - Frontend-specific documentation

## 🔍 API Endpoints

Once the backend is running, you can access:

- `GET /api/health` - Health check endpoint
- `GET /api/data` - Retrieve health monitoring data
- `POST /api/predict` - Make predictions using the ML model
- Additional endpoints documented in the code

## 🧪 Testing

### Backend Tests
```bash
python test_app.py
python test_model_performance.py
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

## 🐳 Docker Deployment

Build and run with Docker:

```bash
docker build -t mlops-health-project .
docker run -p 5000:5000 mlops-health-project
```

## 🔄 MLflow Tracking

To view MLflow experiments:

```bash
mlflow ui
```

Access the MLflow UI at `http://localhost:5000` (or configured port)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is part of an MLOps learning initiative.

## 🆘 Troubleshooting

### Backend Issues
- **Port 5000 already in use**: Change the port in `app.py`
- **Module not found**: Ensure virtual environment is activated and dependencies are installed
- **Database errors**: Check if `health_data.db` exists or needs to be created

### Frontend Issues
- **Port 5173 already in use**: Vite will automatically use the next available port
- **API connection failed**: Verify backend is running on `http://localhost:5000`
- **npm install fails**: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

### General
- Ensure both servers are running simultaneously
- Check firewall settings if localhost connections fail
- Verify Python and Node.js versions meet requirements

## 📧 Contact

For questions or issues, please open an issue in the repository.
