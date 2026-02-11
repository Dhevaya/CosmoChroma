import re
from typing import Tuple
from app.utils.error_handlers import InvalidImageException

def validate_base64_image(image_data: str) -> bool:
    """Validate if string is valid base64 encoded image"""
    if not image_data or not isinstance(image_data, str):
        return False
    
    # Check for common image base64 prefixes
    valid_prefixes = [
        "data:image/jpeg;base64,",
        "data:image/jpg;base64,",
        "data:image/png;base64,"
    ]
    
    has_valid_prefix = any(image_data.startswith(prefix) for prefix in valid_prefixes)
    
    if not has_valid_prefix and not re.match(r'^[A-Za-z0-9+/]*={0,2}$', image_data):
        return False
    
    return True

def validate_image_size(image_size_bytes: int, max_size: int = 10 * 1024 * 1024) -> bool:
    """Validate if image size is within limits"""
    return 0 < image_size_bytes <= max_size

def validate_rgb_values(r: int, g: int, b: int) -> Tuple[bool, str]:
    """Validate RGB color values (0-255)"""
    if not all(0 <= val <= 255 for val in [r, g, b]):
        return False, "RGB values must be between 0 and 255"
    return True, "Valid RGB values"

def validate_hex_color(hex_color: str) -> Tuple[bool, str]:
    """Validate hex color format"""
    if not re.match(r'^#[0-9A-Fa-f]{6}$', hex_color):
        return False, "Invalid hex color format. Expected format: #RRGGBB"
    return True, "Valid hex color"
