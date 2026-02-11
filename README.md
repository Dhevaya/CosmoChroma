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

# 📄 License

CosmoChroma © 2024 - All Rights Reserved

**Built with ❤️ using Python, React, and AI/ML**
