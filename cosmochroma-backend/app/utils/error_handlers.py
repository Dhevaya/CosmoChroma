from fastapi import HTTPException, status
from app.utils.logger import app_logger

class CosmoChromaException(Exception):
    """Base exception for CosmoChroma"""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class InvalidImageException(CosmoChromaException):
    """Raised when image is invalid or unsupported"""
    def __init__(self, message: str = "Invalid image format or corrupted file"):
        super().__init__(message, "INVALID_IMAGE")

class FaceDetectionException(CosmoChromaException):
    """Raised when face detection fails"""
    def __init__(self, message: str = "Could not detect face in image"):
        super().__init__(message, "FACE_NOT_DETECTED")

class SkinAnalysisException(CosmoChromaException):
    """Raised when skin analysis fails"""
    def __init__(self, message: str = "Error during skin analysis"):
        super().__init__(message, "ANALYSIS_FAILED")

class ImageProcessingException(CosmoChromaException):
    """Raised when image processing fails"""
    def __init__(self, message: str = "Error processing image"):
        super().__init__(message, "IMAGE_PROCESSING_FAILED")

def exception_handler(exc: CosmoChromaException):
    """Handle custom exceptions and return HTTP response"""
    app_logger.error(f"{exc.code}: {exc.message}")
    
    status_map = {
        "INVALID_IMAGE": status.HTTP_400_BAD_REQUEST,
        "FACE_NOT_DETECTED": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "ANALYSIS_FAILED": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "IMAGE_PROCESSING_FAILED": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "INTERNAL_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    
    http_status = status_map.get(exc.code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    raise HTTPException(
        status_code=http_status,
        detail={
            "error": exc.code,
            "message": exc.message
        }
    )
