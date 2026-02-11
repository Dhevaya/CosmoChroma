# CosmoChroma Backend API

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
# Development mode with auto-reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using the main script
python main.py
```

### 4. Access Documentation
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/health

## API Endpoints

### POST /api/analyze
Analyze a skin selfie

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file (JPG/PNG, max 10MB)

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
    "confidence_scores": {}
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

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "message": "API is running"
}
```

## Project Structure

```
cosmochroma-backend/
├── app/
│   ├── api/routes/
│   │   ├── analysis.py      # POST /api/analyze
│   │   └── health.py        # GET /api/health
│   ├── models/
│   │   └── skin_analyzer.py # Core analysis logic
│   ├── services/
│   │   ├── image_processor.py
│   │   ├── color_utils.py
│   │   ├── product_recommender.py
│   │   └── routine_builder.py
│   ├── schemas/
│   │   └── response_models.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── error_handlers.py
│   │   └── validators.py
│   └── data/
│       ├── indian_products.json
│       └── undertone_mapping.json
├── tests/
├── main.py
├── config.py
├── requirements.txt
└── .env
```

## Features

- **Image Processing**: Face detection using OpenCV Haar Cascade
- **Skin Tone Analysis**: RGB, HSV, LAB color space analysis
- **Undertone Classification**: Warm Golden, Warm Olive, Cool, Neutral
- **Seasonal Color Type**: Spring, Summer, Autumn, Winter
- **Skin Type Detection**: Oily, Dry, Combination, Sensitive, Normal
- **Product Matching**: Delta-E algorithm for color-accurate recommendations
- **Personalized Routines**: AM/PM/Weekly skincare routines based on skin type
- **Indian Beauty Products**: Recommendations from Nykaa, Sugar Cosmetics, MyGlamm

## Configuration

Edit `config.py` to customize:
- API settings (host, port, debug mode)
- CORS origins
- File upload limits
- Face detection thresholds
- Color analysis parameters

## Technologies

- **Framework**: FastAPI
- **Image Processing**: OpenCV, Pillow
- **Color Analysis**: NumPy, SciPy
- **Face Detection**: OpenCV Haar Cascade, MediaPipe
- **ML/DL**: TensorFlow/PyTorch (ready for integration)

## Development

For local development with hot reload:
```bash
python -m uvicorn main:app --reload
```

## Deployment

### Using Docker
```bash
docker build -f docker/Dockerfile -t cosmochroma-api .
docker run -p 8000:8000 cosmochroma-api
```

### Using Heroku/Railway.app
```bash
# Railway deployment
railway up
```

## Error Handling

The API returns proper HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid image)
- `422`: Unprocessable entity (no face detected)
- `500`: Server error

## Logging

Logs are output to console. Configure in `app/utils/logger.py`.

## License

CosmoChroma © 2024
