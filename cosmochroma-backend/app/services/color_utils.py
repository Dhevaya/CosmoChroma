import numpy as np
from typing import Tuple, Dict
from app.utils.logger import app_logger
import cv2

class ColorUtils:
    """Color conversion and analysis utilities"""
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB values to hex color code"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color code to RGB values"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hsv(r: int, g: int, b: int) -> Dict[str, float]:
        """Convert RGB to HSV color space"""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        max_c = max(r_norm, g_norm, b_norm)
        min_c = min(r_norm, g_norm, b_norm)
        delta = max_c - min_c
        
        # Hue
        if delta == 0:
            h = 0
        elif max_c == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif max_c == g_norm:
            h = 60 * (((b_norm - r_norm) / delta) + 2)
        else:
            h = 60 * (((r_norm - g_norm) / delta) + 4)
        
        # Saturation
        s = 0 if max_c == 0 else (delta / max_c)
        
        # Value
        v = max_c
        
        return {'h': round(h, 2), 's': round(s * 100, 2), 'v': round(v * 100, 2)}
    
    @staticmethod
    def rgb_to_lab(r: int, g: int, b: int) -> Dict[str, float]:
        """Convert RGB to CIELAB color space"""
        # Normalize RGB
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        # Apply gamma correction
        r_lin = r_norm ** 2.4 if r_norm > 0.04045 else r_norm / 12.92
        g_lin = g_norm ** 2.4 if g_norm > 0.04045 else g_norm / 12.92
        b_lin = b_norm ** 2.4 if b_norm > 0.04045 else b_norm / 12.92
        
        # Convert to XYZ
        x = (r_lin * 0.4124 + g_lin * 0.3576 + b_lin * 0.1805) / 0.95047
        y = (r_lin * 0.2126 + g_lin * 0.7152 + b_lin * 0.0722) / 1.00000
        z = (r_lin * 0.0193 + g_lin * 0.1192 + b_lin * 0.9505) / 1.08883
        
        # Convert XYZ to LAB
        delta = 6/29
        x_f = x ** (1/3) if x > delta ** 3 else x / (3 * delta ** 2) + 4/29
        y_f = y ** (1/3) if y > delta ** 3 else y / (3 * delta ** 2) + 4/29
        z_f = z ** (1/3) if z > delta ** 3 else z / (3 * delta ** 2) + 4/29
        
        l = (116 * y_f) - 16
        a = 500 * (x_f - y_f)
        b_lab = 200 * (y_f - z_f)
        
        return {'l': round(l, 2), 'a': round(a, 2), 'b': round(b_lab, 2)}
    
    @staticmethod
    def delta_e_cie76(lab1: Dict[str, float], lab2: Dict[str, float]) -> float:
        """Calculate color difference using CIE76 formula"""
        dl = lab1['l'] - lab2['l']
        da = lab1['a'] - lab2['a']
        db = lab1['b'] - lab2['b']
        
        delta_e = np.sqrt(dl**2 + da**2 + db**2)
        return round(float(delta_e), 2)
    
    @staticmethod
    def delta_e_cie94(lab1: Dict[str, float], lab2: Dict[str, float], 
                      kl: float = 1, kc: float = 1, kh: float = 1) -> float:
        """Calculate color difference using CIE94 formula (more perceptually accurate)"""
        dl = lab1['l'] - lab2['l']
        da = lab1['a'] - lab2['a']
        db = lab1['b'] - lab2['b']
        
        c1 = np.sqrt(lab1['a']**2 + lab1['b']**2)
        c2 = np.sqrt(lab2['a']**2 + lab2['b']**2)
        dc = c1 - c2
        
        dh = np.sqrt(da**2 + db**2 - dc**2)
        
        delta_e = np.sqrt(
            (dl / kl)**2 + 
            (dc / (kc * c1))**2 + 
            (dh / kh)**2
        )
        
        return round(float(delta_e), 2)
    
    @staticmethod
    def extract_dominant_color(region: np.ndarray) -> Tuple[int, int, int]:
        """Extract dominant color from image region with improved accuracy"""
        try:
            import cv2
            
            # Filter out extreme values (shadows and highlights)
            # This helps avoid getting dark shadows or bright reflections
            hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
            
            # Create mask for skin-like colors (exclude pure black and white)
            # Keep values between 30% and 90% brightness
            lower_bound = np.array([0, 0, int(255 * 0.30)])
            upper_bound = np.array([180, 255, int(255 * 0.95)])
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            
            # Apply morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Filter pixels using the mask
            filtered_pixels = region[mask > 0]
            
            if len(filtered_pixels) == 0:
                # If no pixels pass the filter, use the original region
                filtered_pixels = region.reshape((-1, 3))
            else:
                filtered_pixels = filtered_pixels.astype(np.float32)
            
            # K-means clustering to find dominant color
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, _, centers = cv2.kmeans(
                filtered_pixels, 
                1,  # One cluster for dominant color
                None, 
                criteria, 
                10, 
                cv2.KMEANS_RANDOM_CENTERS
            )
            
            dominant_color = centers[0].astype(int)
            # OpenCV uses BGR, convert to RGB
            b, g, r = dominant_color[0], dominant_color[1], dominant_color[2]
            
            # Ensure values are in valid range
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            
            app_logger.info(f"Dominant color extracted (filtered): RGB({r}, {g}, {b})")
            return r, g, b
        
        except Exception as e:
            app_logger.error(f"Error extracting dominant color: {str(e)}")
            # Fallback: average color
            try:
                avg_color = np.mean(region, axis=(0, 1)).astype(int)
                b, g, r = avg_color[0], avg_color[1], avg_color[2]
                return int(r), int(g), int(b)
            except:
                raise
    
    @staticmethod
    def calculate_brightness(r: int, g: int, b: int) -> float:
        """Calculate brightness/luminance of color (0-100)"""
        # Using relative luminance formula
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255 * 100
        return round(brightness, 2)
    
    @staticmethod
    def calculate_saturation(r: int, g: int, b: int) -> float:
        """Calculate saturation of color (0-100)"""
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        
        if max_c == 0:
            return 0.0
        
        saturation = ((max_c - min_c) / max_c) * 100
        return round(saturation, 2)
    
    @staticmethod
    def calculate_warm_score(r: int, g: int, b: int) -> float:
        """
        Calculate warmth score (0-1) with improved accuracy
        Uses LAB color space analysis for perceptual accuracy
        
        Warm: Higher a* values (red-green axis toward red)
        Cool: Lower a* values (red-green axis toward green)
        """
        # Normalize RGB
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        # Apply gamma correction
        r_lin = r_norm ** 2.4 if r_norm > 0.04045 else r_norm / 12.92
        g_lin = g_norm ** 2.4 if g_norm > 0.04045 else g_norm / 12.92
        b_lin = b_norm ** 2.4 if b_norm > 0.04045 else b_norm / 12.92
        
        # Convert to XYZ
        x = (r_lin * 0.4124 + g_lin * 0.3576 + b_lin * 0.1805) / 0.95047
        y = (r_lin * 0.2126 + g_lin * 0.7152 + b_lin * 0.0722) / 1.00000
        z = (r_lin * 0.0193 + g_lin * 0.1192 + b_lin * 0.9505) / 1.08883
        
        # Convert XYZ to LAB
        delta = 6/29
        x_f = x ** (1/3) if x > delta ** 3 else x / (3 * delta ** 2) + 4/29
        y_f = y ** (1/3) if y > delta ** 3 else y / (3 * delta ** 2) + 4/29
        z_f = z ** (1/3) if z > delta ** 3 else z / (3 * delta ** 2) + 4/29
        
        # Use LAB's a* value to determine warmth
        a_value = 500 * (x_f - y_f)
        
        # Normalize a* value to 0-1 scale (-128 to +128 typical range)
        warm_score = (a_value + 128) / 256
        warm_score = max(0, min(1.0, warm_score))  # Clamp to 0-1
        
        return round(warm_score, 2)
    
    @staticmethod
    def calculate_olive_score(r: int, g: int, b: int) -> float:
        """
        Calculate olive undertone score (0-1) with improved accuracy
        Olive has unique greenish hue even in warm tones
        
        Uses hue analysis: Olive appears in yellow-green range (50-120 degrees)
        """
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        max_c = max(r_norm, g_norm, b_norm)
        min_c = min(r_norm, g_norm, b_norm)
        delta = max_c - min_c
        
        # Calculate hue
        if delta == 0:
            h = 0
        elif max_c == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif max_c == g_norm:
            h = 60 * (((b_norm - r_norm) / delta) + 2)
        else:
            h = 60 * (((r_norm - g_norm) / delta) + 4)
        
        # Olive appears in yellow-green range (50-120 degrees)
        # Calculate how much the color fits olive hue range
        if 50 < h < 120:
            olive_score = 1.0 - abs(h - 85) / 70  # Peak at 85 degrees
        else:
            olive_score = 0.0
        
        # Also consider green channel elevation
        if r + b > 0:
            green_elevation = g / (r + b)
            olive_score = max(olive_score, green_elevation / 2)
        
        return round(max(0, min(1.0, olive_score)), 2)
