# CosmoChroma

🌟 AI-Powered Skin Analysis & Beauty Recommendation Platform

Analyze your selfie to get personalized skincare routines and makeup recommendations based on your unique skin tone, undertone, and skin type.

## 🚀 What is CosmoChroma?

CosmoChroma is a full-stack web application that uses:
- **Computer Vision** for accurate skin tone extraction
- **Machine Learning** for skin analysis classification
- **Color Science** (Delta-E algorithm) for perfect product matching
- **AI** to generate personalized skincare routines

### User Journey

1. 📸 Upload your selfie (JPG/PNG)
2. 🤖 AI analyzes your skin in 2-3 seconds
3. 📊 Get comprehensive results including:
   - Exact skin tone (RGB, HSV, Hex)
   - Undertone classification (Warm Golden, Cool, Olive, Neutral)
   - Seasonal color type (Spring, Summer, Autumn, Winter)
   - Skin type (Oily, Dry, Combination, Sensitive, Normal)
   - Personalized morning/evening/weekly skincare routine
   - Top 5 makeup product recommendations

## 🎯 Features

### 🎨 Skin Analysis
- **Accurate Color Extraction**: Detect skin tone from cheek region
- **Undertone Detection**: Identify warm, cool, olive, or neutral undertones
- **Seasonal Color Typing**: Classify into Spring, Summer, Autumn, or Winter
- **Skin Type Analysis**: Determine oily, dry, combination, sensitive, or normal
- **Confidence Scores**: All classifications include confidence percentages

### 💄 Product Recommendations
- **Foundation**: Color-matched foundations with shade preview
- **Blush**: Complementary blush colors and shades
- **Lipstick**: Personalized lipstick recommendations
- **Concealer**: Matching concealer options
- **Eyeshadow**: Coordinated eyeshadow palettes

Each product includes:
- ✨ Product images
- 💰 Price in INR
- ⭐ Rating and review count
- 🔗 Direct buy links
- 📊 Color match accuracy score

### 🧴 Skincare Routines
Personalized routines customized to your skin type:
- **Morning Routine**: Energizing and protective steps
- **Evening Routine**: Cleansing and repair steps
- **Weekly Routine**: Deep care treatments

## 🛠 Technology Stack

### Backend (Python)
- **Framework**: FastAPI
- **Image Processing**: OpenCV, Pillow
- **Color Analysis**: NumPy, SciPy
- **Face Detection**: OpenCV Haar Cascade
- **ML/DL Ready**: TensorFlow integration

### Frontend (React)
- **UI Framework**: React 18
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **State Management**: Zustand
- **HTTP Client**: Axios
- **File Upload**: React Dropzone

### Databases & Services
- **Products Database**: JSON (easily migrable to PostgreSQL)
- **Caching**: In-memory (ready for Redis)
- **Authentication**: Ready for JWT integration

## 📁 Project Structure

```
CosmoChroma/
├── cosmochroma-backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/routes/           # API endpoints
│   │   ├── models/               # ML models and analyzers
│   │   ├── services/             # Business logic
│   │   ├── schemas/              # Request/response models
│   │   ├── utils/                # Utilities
│   │   └── data/                 # Product database
│   ├── tests/                    # Unit tests
│   ├── main.py                   # FastAPI entry point
│   ├── config.py                 # Configuration
│   ├── requirements.txt          # Python dependencies
│   └── README.md
│
├── cosmochroma-frontend/         # React Vite frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/             # API client
│   │   ├── hooks/                # Custom hooks
│   │   ├── store/                # State management
│   │   ├── styles/               # CSS/Tailwind
│   │   ├── App.jsx               # Main app
│   │   └── main.jsx              # React entry
│   ├── public/                   # Static assets
│   ├── index.html                # HTML template
│   ├── package.json              # Dependencies
│   ├── vite.config.js            # Vite config
│   ├── tailwind.config.js        # Tailwind config
│   └── README.md
│
└── README.md                     # This file
```

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd cosmochroma-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload --port 8000
```

**API will be available at**: http://localhost:8000
**Swagger Docs**: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend
cd cosmochroma-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be available at**: http://localhost:3000

### Verify Setup

1. Check backend health:
```bash
curl http://localhost:8000/api/health
```

2. Open frontend: http://localhost:3000
3. Upload a selfie to test the analysis

## 🔬 How It Works

### 1. Image Processing
- Load and validate image
- Detect face using OpenCV Haar Cascade
- Extract cheek region (most accurate for skin tone)
- Apply preprocessing if needed

### 2. Skin Tone Analysis
- Extract dominant color from skin region using K-means clustering
- Convert RGB to multiple color spaces:
  - HSV (for saturation and brightness)
  - LAB (for perceptual color difference)
- Calculate metrics:
  - Brightness/Luminance
  - Saturation
  - Warmth score
  - Olive undertone score

### 3. Classification
- **Undertone**: Based on warm score and olive score thresholds
- **Season**: Combination of brightness, saturation, and undertone
- **Skin Type**: Visual characteristics (can be upgraded to CNN)

### 4. Product Matching
- Load product database with multiple shades
- Calculate Delta-E (CIE94) for each product shade
- Rank by color distance (lower = better match)
- Return top 5 recommendations per category

### 5. Skincare Routine
- Select routine template based on skin type
- Generate personalized steps with timings
- Add product suggestions for each step

## 📊 API Endpoints

### POST /api/analyze
Upload image and get complete analysis

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@selfie.jpg"
```

**Response:**
```json
{
  "skin_analysis": {
    "skin_tone_rgb": {"r": 230, "g": 190, "b": 170},
    "skin_tone_hex": "#E6BEAA",
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

### GET /api/health
Health check endpoint

```bash
curl http://localhost:8000/api/health
```

## 🎯 Key Algorithms

### Delta-E (CIE94)
Color difference calculation for accurate product matching:
```
ΔE = √[(ΔL/Kl)² + (ΔC/Kc)² + (ΔH/Kh)²]
```

### Undertone Detection
```
warm_score = (R + 0.5*G) / (R+G+B)
olive_score = G / (R+B)
```

### Seasonal Classification
Combination of:
- Brightness (luminance)
- Saturation (color intensity)
- Warm score (color temperature)

## 🚢 Deployment

### Backend
- **Heroku**: `git push heroku main`
- **Railway.app**: `railway up`
- **AWS EC2**: Docker container
- **Google Cloud Run**: Serverless

### Frontend
- **Vercel**: `vercel`
- **Netlify**: Drag and drop `dist` folder
- **GitHub Pages**: Static hosting
- **AWS S3**: Static website

## 🔧 Configuration

### Backend Config (`config.py`)
```python
API_TITLE = "CosmoChroma API"
HOST = "0.0.0.0"
PORT = 8000
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
CORS_ORIGINS = ["http://localhost:3000", ...]
```

### Frontend Config (`.env`)
```
VITE_API_URL=http://localhost:8000
```

## 📦 Dependencies

### Backend
- fastapi==0.104.1
- opencv-python==4.8.1.78
- tensorflow==2.14.0
- numpy==1.24.3
- scipy==1.11.4
- pydantic==2.5.0

### Frontend
- react@18.2.0
- tailwindcss@3.3.0
- axios@1.6.0
- zustand@4.4.0
- vite@5.0.0

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 already in use**: `lsof -i :8000` then `kill -9 <PID>`
- **OpenCV not found**: `pip install opencv-python`
- **Face detection fails**: Ensure clear, well-lit selfie

### Frontend Issues
- **API not reachable**: Check backend is running on port 8000
- **CORS errors**: Verify CORS_ORIGINS in backend config
- **Styles not loading**: Run `npm install` and `npm run dev`

## 🔐 Security

- Input validation on all API endpoints
- File type and size validation
- CORS protection
- Error messages don't expose sensitive info
- Ready for JWT authentication

## 📈 Future Enhancements

- [ ] User accounts and history
- [ ] Advanced CNN for skin type detection
- [ ] Virtual makeup try-on
- [ ] Dermatologist consultation integration
- [ ] Mobile app (React Native)
- [ ] Real-time video analysis
- [ ] Skin condition detection (acne, sensitivity, etc.)
- [ ] Ingredient database and allergy alerts
- [ ] Subscription-based premium features

## 📄 License

CosmoChroma © 2024 - All Rights Reserved

## 👨‍💻 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check README files in backend/frontend folders
- Review API documentation at `/docs`

---

**Built with ❤️ using Python, React, and AI/ML**
