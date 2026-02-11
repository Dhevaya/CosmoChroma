import numpy as np
from app.services.color_utils import ColorUtils
from app.schemas.response_models import UndertoneEnum, SeasonEnum, SkinTypeEnum
from app.utils.logger import app_logger

class SkinAnalyzer:
    """Analyze skin tone, undertone, season, and type"""
    
    def __init__(self):
        self.color_utils = ColorUtils()
        self.app_logger = app_logger
    
    def analyze_skin_tone(self, r: int, g: int, b: int) -> dict:
        """Analyze skin tone and extract color information"""
        try:
            analysis = {
                'rgb': {'r': r, 'g': g, 'b': b},
                'hex': self.color_utils.rgb_to_hex(r, g, b),
                'hsv': self.color_utils.rgb_to_hsv(r, g, b),
                'lab': self.color_utils.rgb_to_lab(r, g, b),
                'brightness': self.color_utils.calculate_brightness(r, g, b),
                'saturation': self.color_utils.calculate_saturation(r, g, b),
                'warm_score': self.color_utils.calculate_warm_score(r, g, b),
                'olive_score': self.color_utils.calculate_olive_score(r, g, b),
            }
            
            self.app_logger.info(f"Skin tone analyzed: {analysis['hex']}")
            return analysis
        
        except Exception as e:
            self.app_logger.error(f"Error analyzing skin tone: {str(e)}")
            raise
    
    def classify_undertone(self, warm_score: float, olive_score: float) -> tuple:
        """
        Classify undertone based on warm and olive scores with improved accuracy
        
        Returns:
            tuple: (undertone, confidence_score)
        """
        # Enhanced thresholds based on more granular analysis
        warm_threshold_cool = 0.40
        warm_threshold_neutral = 0.50
        warm_threshold_golden = 0.60
        olive_threshold = 0.65
        
        # Calculate confidence scores with weighted components
        confidence_scores = {}
        
        # Warm Golden: High warm score, low olive
        warm_golden_score = warm_score * 100 if warm_score > warm_threshold_golden else 0
        confidence_scores['warm_golden'] = warm_golden_score
        
        # Warm Olive: High warm and high olive
        warm_olive_score = min(warm_score, olive_score) * 100 if (warm_score > warm_threshold_golden and olive_score > olive_threshold) else 0
        confidence_scores['warm_olive'] = warm_olive_score
        
        # Cool: Low warm, low olive
        cool_score = (1 - warm_score) * 100 if warm_score < warm_threshold_cool else 0
        confidence_scores['cool'] = cool_score
        
        # Neutral: Medium warm, low olive
        neutral_score = (1 - abs(warm_score - 0.5) * 2) * 100 if (warm_threshold_cool < warm_score < warm_threshold_golden and olive_score < olive_threshold) else 0
        confidence_scores['neutral'] = neutral_score
        
        # Determine undertone based on highest confidence
        best_undertone = max(confidence_scores.items(), key=lambda x: x[1])
        undertone_name = best_undertone[0]
        confidence = min(best_undertone[1], 100)
        
        # Map string to enum
        undertone_map = {
            'warm_golden': UndertoneEnum.WARM_GOLDEN,
            'warm_olive': UndertoneEnum.WARM_OLIVE,
            'cool': UndertoneEnum.COOL,
            'neutral': UndertoneEnum.NEUTRAL
        }
        undertone = undertone_map[undertone_name]
        
        self.app_logger.info(f"Undertone classified: {undertone} (confidence: {confidence:.2f}%) | Scores: {confidence_scores}")
        return undertone, round(confidence, 2)
    
    def classify_season(self, brightness: float, saturation: float, 
                       warm_score: float, undertone: UndertoneEnum) -> tuple:
        """
        Classify seasonal color type with improved accuracy
        
        Spring: Light + warm + clear/high saturation
        Summer: Light/Medium + cool + muted/low saturation
        Autumn: Medium/Deep + warm + muted/low saturation
        Winter: Medium/Deep + cool + high contrast/saturation
        
        Returns:
            tuple: (season, confidence_score)
        """
        confidence_scores = {}
        
        # Spring: Light skin, warm, clear colors (high saturation)
        spring_score = 0
        if brightness > 65:
            spring_score += 35  # Light is key for spring
        if warm_score > 0.55:
            spring_score += 35  # Warm is key for spring
        if saturation > 55:
            spring_score += 30  # Clear/bright colors
        confidence_scores['Spring'] = spring_score
        
        # Summer: Light/Medium, cool, soft/muted (low saturation)
        summer_score = 0
        if 45 < brightness < 75:
            summer_score += 30
        if warm_score < 0.50:
            summer_score += 35  # Cool is key for summer
        if saturation < 65:
            summer_score += 35  # Muted/soft colors
        confidence_scores['Summer'] = summer_score
        
        # Autumn: Medium/Deep, warm, muted (low saturation)
        autumn_score = 0
        if brightness > 35:
            autumn_score += 25
        if warm_score > 0.55:
            autumn_score += 35  # Warm is key for autumn
        if saturation < 70:
            autumn_score += 40  # Muted is key for autumn
        confidence_scores['Autumn'] = autumn_score
        
        # Winter: Medium/Deep, cool, high contrast (high saturation)
        winter_score = 0
        if brightness < 70:
            winter_score += 30
        if warm_score < 0.50:
            winter_score += 35  # Cool is key for winter
        if saturation > 45:
            winter_score += 35  # High contrast/clear colors
        confidence_scores['Winter'] = winter_score
        
        # Get season with highest score
        season_str = max(confidence_scores, key=confidence_scores.get)
        season = SeasonEnum(season_str)
        confidence = round(confidence_scores[season_str], 2)
        
        # Ensure at least some confidence level
        if confidence < 30:
            confidence = max(30, confidence)
        
        self.app_logger.info(f"Season classified: {season} (confidence: {confidence}) | Scores: {confidence_scores}")
        return season, confidence
    
    def classify_skin_type(self, brightness: float, saturation: float) -> tuple:
        """
        Classify skin type with improved accuracy
        
        Oily: High saturation and brightness (reflects light)
        Dry: Low saturation, lower brightness (dull appearance)
        Combination: Mixed characteristics
        Sensitive: Moderate values with uneven tone
        Normal: Well-balanced brightness and saturation
        
        Returns:
            tuple: (skin_type, confidence_score)
        """
        confidence_scores = {}
        
        # Oily: High saturation (reflects light) and brightness
        oily_score = 0
        if saturation > 70:
            oily_score += 45
        if brightness > 65:
            oily_score += 45
        if 50 < saturation < 85 and 60 < brightness < 80:
            oily_score += 10
        confidence_scores['oily'] = oily_score
        
        # Dry: Low saturation (matte), lower brightness
        dry_score = 0
        if saturation < 45:
            dry_score += 45
        if brightness < 55:
            dry_score += 45
        if 25 < saturation < 50 and 40 < brightness < 60:
            dry_score += 10
        confidence_scores['dry'] = dry_score
        
        # Combination: Mixed characteristics (medium-high saturation, medium brightness)
        combination_score = 0
        if 50 < saturation < 75:
            combination_score += 40
        if 50 < brightness < 70:
            combination_score += 40
        if saturation > 50 or brightness > 55:  # Tendency toward oily in some areas
            combination_score += 20
        confidence_scores['combination'] = combination_score
        
        # Normal: Well-balanced, healthy appearance
        normal_score = 0
        if 50 < brightness < 75:
            normal_score += 35
        if 50 < saturation < 70:
            normal_score += 35
        if 50 < brightness < 70 and 50 < saturation < 70:
            normal_score += 30
        confidence_scores['normal'] = normal_score
        
        # Sensitive: Moderate with signs of sensitivity
        sensitive_score = 0
        if 45 < brightness < 70 and 40 < saturation < 65:
            sensitive_score += 50
        if 55 < brightness < 68 and 45 < saturation < 62:
            sensitive_score += 50
        confidence_scores['sensitive'] = sensitive_score
        
        # Get type with highest score
        skin_type_str = max(confidence_scores, key=confidence_scores.get)
        skin_type = SkinTypeEnum(skin_type_str)
        confidence = round(confidence_scores[skin_type_str], 2)
        
        # Ensure minimum confidence
        if confidence < 40:
            confidence = max(40, confidence)
        
        self.app_logger.info(f"Skin type classified: {skin_type} (confidence: {confidence}) | Scores: {confidence_scores}")
        return skin_type, confidence
    
    def analyze_complete(self, r: int, g: int, b: int) -> dict:
        """Complete skin analysis"""
        try:
            # Analyze skin tone
            tone_analysis = self.analyze_skin_tone(r, g, b)
            
            # Classify undertone
            undertone, undertone_confidence = self.classify_undertone(
                tone_analysis['warm_score'],
                tone_analysis['olive_score']
            )
            
            # Classify season
            season, season_confidence = self.classify_season(
                tone_analysis['brightness'],
                tone_analysis['saturation'],
                tone_analysis['warm_score'],
                undertone
            )
            
            # Classify skin type
            skin_type, skin_type_confidence = self.classify_skin_type(
                tone_analysis['brightness'],
                tone_analysis['saturation']
            )
            
            return {
                'skin_tone': tone_analysis,
                'undertone': undertone,
                'undertone_confidence': undertone_confidence,
                'season': season,
                'season_confidence': season_confidence,
                'skin_type': skin_type,
                'skin_type_confidence': skin_type_confidence,
                'confidence_scores': {
                    'undertone': undertone_confidence,
                    'season': season_confidence,
                    'skin_type': skin_type_confidence,
                }
            }
        
        except Exception as e:
            self.app_logger.error(f"Complete analysis failed: {str(e)}")
            raise
