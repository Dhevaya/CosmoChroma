# CosmoChroma - Complete Setup & Deployment Guide

## 📋 Overview

CosmoChroma is a full-stack AI-powered skin analysis platform built with:
- **Backend**: Python + FastAPI + OpenCV + TensorFlow
- **Frontend**: React 18 + Tailwind CSS + Vite
- **Database**: JSON (easily upgradable to PostgreSQL)

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Backend Setup

```bash
cd cosmochroma-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload --port 8000
```

✅ Backend ready at: http://localhost:8000
📚 API Docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd cosmochroma-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend ready at: http://localhost:3000

## 📁 Project Structure

### Backend Structure

```
cosmochroma-backend/
├── app/
│   ├── api/routes/
│   │   ├── analysis.py         # Main analysis endpoint
│   │   └── health.py           # Health check
│   ├── models/
│   │   └── skin_analyzer.py    # Core analysis logic
│   ├── services/
│   │   ├── image_processor.py  # Face detection & extraction
│   │   ├── color_utils.py      # Color space conversions
│   │   ├── product_recommender.py  # Product matching
│   │   └── routine_builder.py  # Routine generation
│   ├── schemas/
│   │   └── response_models.py  # Pydantic models
│   ├── utils/
│   │   ├── logger.py           # Logging
│   │   ├── error_handlers.py   # Exception handling
│   │   └── validators.py       # Input validation
│   └── data/
│       └── indian_products.json # Product database
├── main.py                      # FastAPI app
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
└── docker/                      # Docker files
```

### Frontend Structure

```
cosmochroma-frontend/
├── src/
│   ├── components/
│   │   ├── UploadForm.jsx              # Image upload
│   │   ├── SkinToneResults.jsx         # Analysis display
│   │   ├── ProductRecommendations.jsx  # Product cards
│   │   ├── SkincareRoutine.jsx         # Routine display
│   │   └── ResultsDashboard.jsx        # Results page
│   ├── services/
│   │   └── api.js                      # API client
│   ├── hooks/
│   │   └── useImageAnalysis.js         # Analysis hook
│   ├── store/
│   │   └── analysisStore.js            # State management
│   ├── styles/
│   │   └── globals.css                 # Global styles
│   ├── App.jsx                         # Main component
│   └── main.jsx                        # React entry
├── index.html                          # HTML template
├── vite.config.js                      # Vite config
├── tailwind.config.js                  # Tailwind config
└── package.json                        # Dependencies
```

## 🔧 Configuration

### Backend Configuration (`config.py`)

```python
# API Settings
API_TITLE = "CosmoChroma API"
API_VERSION = "1.0.0"
DEBUG = True
HOST = "0.0.0.0"
PORT = 8000

# CORS Configuration (for frontend)
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

# File Upload
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Face Detection
FACE_DETECTION_MIN_CONFIDENCE = 0.5
TARGET_IMAGE_SIZE = (640, 480)
```

### Frontend Configuration (`.env`)

```
VITE_API_URL=http://localhost:8000
```

## 📊 API Endpoints

### 1. POST /api/analyze
Upload image and get complete analysis

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@your_selfie.jpg"
```

**Response:**
```json
{
  "skin_analysis": {
    "skin_tone_rgb": {"r": 230, "g": 190, "b": 170},
    "skin_tone_hex": "#E6BEAA",
    "skin_tone_hsv": {"h": 20.5, "s": 26.1, "v": 90.2},
    "undertone": "warm_golden",
    "season": "Spring",
    "skin_type": "normal",
    "confidence_scores": {...}
  },
  "foundation_recommendations": [...],
  "blush_recommendations": [...],
  "lipstick_recommendations": [...],
  "concealer_recommendations": [...],
  "eyeshadow_recommendations": [...],
  "morning_routine": {...},
  "evening_routine": {...},
  "weekly_routine": {...},
  "analysis_timestamp": "2024-01-01T12:00:00"
}
```

### 2. GET /api/health
Health check

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "message": "API is running"
}
```

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` → `kill -9 <PID>` |
| OpenCV import error | `pip install opencv-python` |
| Face not detected | Ensure good lighting and clear face |
| CORS error | Check CORS_ORIGINS in config.py |
| API not responding | Verify backend is running: `curl http://localhost:8000/api/health` |
| Dependencies fail | Delete `venv/` and reinstall: `pip install -r requirements.txt` |

## 🚢 Deployment

### Backend Deployment

#### Using Railway.app (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link project
railway login
railway link

# Deploy
railway up
```

#### Using Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create cosmochroma-api

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

#### Using Docker
```bash
# Build image
docker build -f docker/Dockerfile -t cosmochroma-api .

# Run container
docker run -p 8000:8000 cosmochroma-api

# Or use docker-compose
docker-compose -f docker/docker-compose.yml up
```

### Frontend Deployment

#### Using Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# VITE_API_URL=your_backend_url
```

#### Using Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod --dir=dist

# Or drag dist folder to Netlify dashboard
```

#### Using GitHub Pages
```bash
# Add to vite.config.js
export default {
  base: '/cosmochroma/',
  // ...
}

# Build and deploy
npm run build
```

## 🔐 Security Best Practices

### Backend
- ✅ Input validation on all endpoints
- ✅ File type and size restrictions
- ✅ CORS protection
- ✅ Error messages don't expose sensitive info
- 🔜 Add JWT authentication
- 🔜 Rate limiting
- 🔜 HTTPS in production

### Frontend
- ✅ Environment variables for API URL
- ✅ No hardcoded credentials
- ✅ Input validation before API calls
- 🔜 Add authentication tokens
- 🔜 Implement CSRF protection

## 📈 Performance Optimization

### Backend
- Use caching for product database
- Optimize image processing pipeline
- Implement async operations
- Add request compression

### Frontend
- Code splitting with React.lazy()
- Image lazy loading
- CSS tree shaking
- Minify production build

## 🧪 Testing

### Backend Testing
```bash
pytest tests/
pytest --cov=app tests/
```

### Frontend Testing
```bash
npm run test
```

## 📦 Database Setup (Optional)

### Upgrade from JSON to PostgreSQL

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE cosmochroma;
CREATE USER cosmochroma_user WITH PASSWORD 'secure_password';
ALTER ROLE cosmochroma_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE cosmochroma TO cosmochroma_user;
```

3. Update `config.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/cosmochroma"
```

4. Install SQLAlchemy:
```bash
pip install sqlalchemy psycopg2-binary alembic
```

## 🔗 Environment Variables

### Backend (.env)
```
API_TITLE=CosmoChroma API
API_VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./cosmochroma.db
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend-url.com
VITE_APP_NAME=CosmoChroma
```

## 📚 API Documentation

### Swagger UI
- Available at: `http://localhost:8000/docs`
- Interactive API testing
- Real-time documentation

### ReDoc
- Available at: `http://localhost:8000/redoc`
- Clean, readable documentation

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

## 📄 License

CosmoChroma © 2024 - All Rights Reserved

## 📞 Support

- 🐛 Issues: Open GitHub issue
- 💬 Discussions: GitHub Discussions
- 📧 Email: support@cosmochroma.com
- 📖 Docs: Check README files in each folder

## 🎯 Roadmap

- [ ] User authentication and profiles
- [ ] Advanced CNN for skin type detection
- [ ] Virtual makeup try-on with AR
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time video analysis
- [ ] Dermatologist consultation booking
- [ ] Product reviews and ratings
- [ ] Subscription premium features
- [ ] Multi-language support
- [ ] Machine learning model improvements

## 💡 Tips & Tricks

### Development
- Use `--reload` flag for hot reloading in FastAPI
- Use `npm run dev` for hot module replacement in React
- Check API docs at `/docs` while developing

### Performance
- Image preprocessing takes ~500ms
- Analysis takes ~1-2 seconds
- Product matching takes ~300ms

### Customization
- Edit product database: `app/data/indian_products.json`
- Customize routines: `app/services/routine_builder.py`
- Adjust color thresholds: `app/models/skin_analyzer.py`
- Change UI colors: `tailwind.config.js`

---

**Happy analyzing! 🌟**
