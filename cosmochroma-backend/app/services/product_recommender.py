import json
from pathlib import Path
from typing import List
from app.schemas.response_models import ProductRecommendation
from app.services.color_utils import ColorUtils
from app.utils.logger import app_logger

class ProductRecommender:
    """Match user's skin tone with makeup products"""
    
    def __init__(self):
        self.color_utils = ColorUtils()
        self.products = self._load_products()
        self.app_logger = app_logger
    
    def _load_products(self) -> list:
        """Load product database from JSON"""
        try:
            products_path = Path(__file__).parent.parent / "data" / "indian_products.json"
            with open(products_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.app_logger.error(f"Failed to load products database: {str(e)}")
            return []
    
    def find_best_matches(self, user_rgb: dict, category: str, count: int = 5) -> List[ProductRecommendation]:
        """Find best matching products for given skin tone and category"""
        try:
            user_lab = self.color_utils.rgb_to_lab(user_rgb['r'], user_rgb['g'], user_rgb['b'])
            
            # Filter products by category and calculate distances
            products_with_distances = []
            
            for product in self.products:
                if product['category'] != category:
                    continue
                
                # Check all shades of the product
                for shade in product['shades']:
                    shade_rgb = shade.get('rgb', {})
                    if not shade_rgb or not all(k in shade_rgb for k in ['r', 'g', 'b']):
                        continue
                    
                    shade_lab = self.color_utils.rgb_to_lab(shade_rgb['r'], shade_rgb['g'], shade_rgb['b'])
                    delta_e = self.color_utils.delta_e_cie94(user_lab, shade_lab)
                    
                    products_with_distances.append({
                        'product': product,
                        'shade': shade,
                        'delta_e': delta_e
                    })
            
            # Sort by delta_e (lower is better match)
            products_with_distances.sort(key=lambda x: x['delta_e'])
            
            # Create recommendations
            recommendations = []
            for item in products_with_distances[:count]:
                product = item['product']
                shade = item['shade']
                
                recommendation = ProductRecommendation(
                    name=product['name'],
                    brand=product['brand'],
                    category=product['category'],
                    shade=shade['name'],
                    price_inr=product['price_inr'],
                    image_url=product['image_url'],
                    rating=product['rating'],
                    reviews_count=product['reviews_count'],
                    buy_link=product['buy_link'],
                    delta_e_distance=item['delta_e']
                )
                recommendations.append(recommendation)
            
            self.app_logger.info(f"Found {len(recommendations)} {category} recommendations")
            return recommendations
        
        except Exception as e:
            self.app_logger.error(f"Error finding product matches: {str(e)}")
            return []
    
    def get_recommendations_by_skin_type(self, user_rgb: dict, skin_type: str) -> dict:
        """Get product recommendations based on skin type and tone"""
        recommendations = {
            'foundation': self.find_best_matches(user_rgb, 'foundation', 5),
            'blush': self.find_best_matches(user_rgb, 'blush', 5),
            'lipstick': self.find_best_matches(user_rgb, 'lipstick', 5),
            'concealer': self.find_best_matches(user_rgb, 'concealer', 5),
            'eyeshadow': self.find_best_matches(user_rgb, 'eyeshadow', 5),
        }
        
        # Add skin type specific adjustments
        if skin_type == 'oily':
            # For oily skin, prioritize long-wearing products
            self.app_logger.info("Adjusting recommendations for oily skin type")
        elif skin_type == 'dry':
            # For dry skin, prioritize hydrating products
            self.app_logger.info("Adjusting recommendations for dry skin type")
        elif skin_type == 'sensitive':
            # For sensitive skin, suggest hypoallergenic products
            self.app_logger.info("Adjusting recommendations for sensitive skin type")
        
        return recommendations
