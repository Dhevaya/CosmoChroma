from fastapi import APIRouter, File, UploadFile, HTTPException, status
from datetime import datetime
from app.schemas.response_models import AnalysisResultsResponse, SkinAnalysisResponse
from app.services.image_processor import ImageProcessor
from app.services.color_utils import ColorUtils
from app.models.skin_analyzer import SkinAnalyzer
from app.services.product_recommender import ProductRecommender
from app.services.routine_builder import RoutineBuilder
from app.utils.logger import app_logger
from app.utils.error_handlers import InvalidImageException, FaceDetectionException
from config import settings

router = APIRouter(
    prefix="/api",
    tags=["analysis"]
)

# Initialize components
image_processor = ImageProcessor()
color_utils = ColorUtils()
skin_analyzer = SkinAnalyzer()
product_recommender = ProductRecommender()
routine_builder = RoutineBuilder()

@router.post("/analyze", response_model=AnalysisResultsResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze a skin selfie and provide comprehensive results
    
    - **file**: JPG or PNG image file (max 10MB)
    
    Returns complete analysis with skin tone, undertone, season, skin type,
    personalized skincare routine, and makeup recommendations
    """
    try:
        # Validate file
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise InvalidImageException(f"Unsupported image format: {file.content_type}")
        
        # Read and validate file size
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise InvalidImageException(f"File size exceeds {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB limit")
        
        # Convert to base64
        import base64
        image_data = base64.b64encode(content).decode('utf-8')
        
        # Load image
        image = image_processor.load_image_from_base64(image_data)
        
        # Validate image
        if not image_processor.validate_image(image):
            raise InvalidImageException("Invalid image format or corrupted data")
        
        # Detect face
        face_coords = image_processor.detect_face(image)
        
        # Extract skin region
        skin_region = image_processor.extract_skin_region(image, face_coords)
        
        # Extract dominant color
        r, g, b = color_utils.extract_dominant_color(skin_region)
        
        # Complete skin analysis
        analysis_data = skin_analyzer.analyze_complete(r, g, b)
        
        # Create skin analysis response
        skin_analysis = SkinAnalysisResponse(
            skin_tone_rgb=analysis_data['skin_tone']['rgb'],
            skin_tone_hex=analysis_data['skin_tone']['hex'],
            skin_tone_hsv=analysis_data['skin_tone']['hsv'],
            undertone=analysis_data['undertone'],
            season=analysis_data['season'],
            skin_type=analysis_data['skin_type'],
            confidence_scores=analysis_data['confidence_scores']
        )
        
        # Get product recommendations
        product_recs = product_recommender.get_recommendations_by_skin_type(
            analysis_data['skin_tone']['rgb'],
            analysis_data['skin_type'].value
        )
        
        # Build skincare routines
        routines = routine_builder.build_all_routines(analysis_data['skin_type'].value)
        
        # Compile complete results
        results = AnalysisResultsResponse(
            skin_analysis=skin_analysis,
            foundation_recommendations=product_recs['foundation'],
            blush_recommendations=product_recs['blush'],
            lipstick_recommendations=product_recs['lipstick'],
            concealer_recommendations=product_recs['concealer'],
            eyeshadow_recommendations=product_recs['eyeshadow'],
            morning_routine=routines['morning'],
            evening_routine=routines['evening'],
            weekly_routine=routines['weekly'],
            analysis_timestamp=datetime.utcnow().isoformat()
        )
        
        app_logger.info(f"Analysis completed successfully at {results.analysis_timestamp}")
        return results
    
    except InvalidImageException as e:
        app_logger.error(f"Invalid image: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": e.code, "message": e.message}
        )
    except FaceDetectionException as e:
        app_logger.error(f"Face detection failed: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": e.code, "message": e.message}
        )
    except Exception as e:
        app_logger.error(f"Unexpected error during analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "ANALYSIS_FAILED", "message": "An error occurred during analysis. Please try again."}
        )
