# PharmaCode

AI-powered pharmacogenomics learning tool using Google DeepMind's AlphaGenome.

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and add your AlphaGenome API key (optional for demo)
3. Run with Docker: `docker-compose up -d`
4. Access the app at http://localhost:3000

## Development Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Features

- Interactive genetic variant exploration
- Real-time AlphaGenome predictions (or mock data for development)
- Educational pharmacogenomics modules
- Clinical translation of molecular effects

## Note

The app works without an AlphaGenome API key using mock predictions for development.
Add your API key to `.env` for real predictions.
