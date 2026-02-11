import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from app.utils.logger import app_logger
from app.utils.error_handlers import InvalidImageException, FaceDetectionException, ImageProcessingException

class ImageProcessor:
    """Handle image loading, face detection, and skin region extraction"""
    
    def __init__(self):
        # Load pre-trained Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        if self.face_cascade.empty():
            app_logger.warning("Failed to load Haar Cascade classifier")
        
        self.app_logger = app_logger
    
    def load_image_from_base64(self, image_data: str) -> np.ndarray:
        """Load image from base64 encoded string"""
        try:
            # Remove data URI prefix if present
            if "," in image_data:
                image_data = image_data.split(",")[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array and BGR for OpenCV
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            self.app_logger.info(f"Image loaded successfully. Shape: {image_cv.shape}")
            
            return image_cv
        
        except Exception as e:
            self.app_logger.error(f"Failed to load image: {str(e)}")
            raise InvalidImageException(f"Failed to process image: {str(e)}")
    
    def detect_face(self, image: np.ndarray) -> dict:
        """Detect face in image with improved sensitivity"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces with improved parameters
            # Lower minNeighbors for better detection, but still avoid false positives
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,  # Finer scale steps for better detection
                minNeighbors=4,     # Slightly lower to catch faces
                minSize=(50, 50),   # Minimum face size
                maxSize=(min(gray.shape) // 2, min(gray.shape) // 2)  # Maximum face size
            )
            
            if len(faces) == 0:
                raise FaceDetectionException("No face detected in the image")
            
            # Use the largest face (most likely the main subject)
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            
            # Add padding to face detection for better analysis
            padding = int(w * 0.1)
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            self.app_logger.info(f"Face detected at ({x}, {y}) with size ({w}x{h})")
            
            return {
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'confidence': 0.85
            }
        
        except FaceDetectionException:
            raise
        except Exception as e:
            self.app_logger.error(f"Face detection failed: {str(e)}")
            raise FaceDetectionException(f"Error during face detection: {str(e)}")
    
    def extract_skin_region(self, image: np.ndarray, face_coords: dict) -> np.ndarray:
        """Extract skin region (cheeks and forehead) from detected face with improved sampling"""
        try:
            x, y, w, h = face_coords['x'], face_coords['y'], face_coords['width'], face_coords['height']
            
            # Extract multiple skin regions with consistent sizing
            # Forehead region (often cleanest, less makeup)
            forehead_y_start = int(y + h * 0.15)
            forehead_y_end = int(y + h * 0.35)
            forehead_x_start = int(x + w * 0.25)
            forehead_x_end = int(x + w * 0.75)
            
            forehead = image[forehead_y_start:forehead_y_end, forehead_x_start:forehead_x_end]
            
            # Cheek region (center of face)
            cheek_y_start = int(y + h * 0.35)
            cheek_y_end = int(y + h * 0.65)
            cheek_x_start = int(x + w * 0.15)
            cheek_x_end = int(x + w * 0.85)
            
            cheeks = image[cheek_y_start:cheek_y_end, cheek_x_start:cheek_x_end]
            
            # Use forehead as primary (cleaner), fall back to cheeks if needed
            if forehead.size > 0 and forehead.shape[0] > 0 and forehead.shape[1] > 0:
                skin_region = forehead
            elif cheeks.size > 0 and cheeks.shape[0] > 0 and cheeks.shape[1] > 0:
                skin_region = cheeks
            else:
                raise ImageProcessingException("Could not extract skin regions")
            
            self.app_logger.info(f"Skin region extracted. Shape: {skin_region.shape}")
            return skin_region
        
        except ImageProcessingException:
            raise
        except Exception as e:
            self.app_logger.error(f"Skin region extraction failed: {str(e)}")
            raise ImageProcessingException(f"Error extracting skin region: {str(e)}")
    
    def resize_image(self, image: np.ndarray, target_size: tuple = (640, 480)) -> np.ndarray:
        """Resize image to target size"""
        try:
            resized = cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)
            self.app_logger.info(f"Image resized to {target_size}")
            return resized
        except Exception as e:
            raise ImageProcessingException(f"Error resizing image: {str(e)}")
    
    def validate_image(self, image: np.ndarray) -> bool:
        """Validate image format and content"""
        try:
            if image is None or image.size == 0:
                return False
            
            if len(image.shape) not in [2, 3]:
                return False
            
            if image.dtype != np.uint8:
                return False
            
            return True
        except Exception as e:
            self.app_logger.error(f"Image validation failed: {str(e)}")
            return False
