from typing import List
from app.schemas.response_models import SkincareRoutine, SkincareStep
from app.utils.logger import app_logger

class RoutineBuilder:
    """Generate personalized skincare routines based on skin type"""
    
    def __init__(self):
        self.app_logger = app_logger
        self.routines = self._initialize_routines()
    
    def _initialize_routines(self) -> dict:
        """Initialize routine templates"""
        return {
            'oily': {
                'morning': [
                    {'order': 1, 'step_name': 'Cleanser', 'description': 'Use a gel or foam cleanser to remove excess oil and impurities', 'duration': 2, 'products': ['Facewash', 'Gel Cleanser']},
                    {'order': 2, 'step_name': 'Toner', 'description': 'Apply alcohol-free toner to balance pH and remove remaining dirt', 'duration': 2, 'products': ['Toner', 'Clarifying Toner']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Apply lightweight, oil-free serum with niacinamide or salicylic acid', 'duration': 2, 'products': ['Niacinamide Serum', 'BHA Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Use lightweight, water-based moisturizer to keep skin hydrated', 'duration': 2, 'products': ['Gel Moisturizer', 'Lightweight Lotion']},
                    {'order': 5, 'step_name': 'Sunscreen', 'description': 'Apply SPF 30+ sunscreen to protect from UV damage', 'duration': 2, 'products': ['Sunscreen SPF 30+']},
                ],
                'evening': [
                    {'order': 1, 'step_name': 'Cleanser', 'description': 'Use a gentle makeup remover followed by cleanser', 'duration': 3, 'products': ['Makeup Remover', 'Facewash']},
                    {'order': 2, 'step_name': 'Toner', 'description': 'Apply toner to balance skin pH', 'duration': 1, 'products': ['Toner']},
                    {'order': 3, 'step_name': 'Treatment', 'description': 'Apply acne-fighting treatment (BHA, AHA, or retinoid)', 'duration': 3, 'products': ['Salicylic Acid Treatment', 'Retinol']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Use lightweight night moisturizer', 'duration': 2, 'products': ['Light Night Cream', 'Gel Moisturizer']},
                ],
                'weekly': [
                    {'order': 1, 'step_name': 'Exfoliator', 'description': 'Use gentle chemical exfoliator 1-2 times per week', 'duration': 5, 'products': ['BHA Exfoliant', 'Gentle Scrub']},
                    {'order': 2, 'step_name': 'Clay Mask', 'description': 'Apply purifying clay mask to remove excess oil and unclog pores', 'duration': 10, 'products': ['Clay Mask', 'Purifying Mask']},
                    {'order': 3, 'step_name': 'Hydrating Mask', 'description': 'Follow with hydrating sheet mask to balance skin', 'duration': 15, 'products': ['Sheet Mask', 'Hydrating Mask']},
                ]
            },
            'dry': {
                'morning': [
                    {'order': 1, 'step_name': 'Gentle Cleanser', 'description': 'Use a creamy or oil-based cleanser to avoid stripping natural oils', 'duration': 2, 'products': ['Cream Cleanser', 'Oil Cleanser']},
                    {'order': 2, 'step_name': 'Hydrating Toner', 'description': 'Apply hydrating toner with humectants like glycerin', 'duration': 2, 'products': ['Hydrating Toner', 'Essence']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Use hydrating serum with hyaluronic acid or peptides', 'duration': 2, 'products': ['Hyaluronic Acid Serum', 'Hydrating Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Apply rich cream moisturizer to lock in hydration', 'duration': 2, 'products': ['Rich Cream', 'Moisturizing Lotion']},
                    {'order': 5, 'step_name': 'Sunscreen', 'description': 'Apply SPF 30+ sunscreen', 'duration': 2, 'products': ['Sunscreen SPF 30+']},
                ],
                'evening': [
                    {'order': 1, 'step_name': 'Gentle Cleanser', 'description': 'Use creamy cleanser to gently remove makeup', 'duration': 3, 'products': ['Cream Cleanser', 'Makeup Remover']},
                    {'order': 2, 'step_name': 'Hydrating Toner', 'description': 'Apply hydrating toner', 'duration': 2, 'products': ['Hydrating Toner']},
                    {'order': 3, 'step_name': 'Treatment', 'description': 'Apply hydrating treatment or facial oil', 'duration': 3, 'products': ['Facial Oil', 'Hydrating Serum']},
                    {'order': 4, 'step_name': 'Night Cream', 'description': 'Apply rich night cream or sleeping mask', 'duration': 2, 'products': ['Night Cream', 'Sleeping Mask']},
                ],
                'weekly': [
                    {'order': 1, 'step_name': 'Hydrating Mask', 'description': 'Use hydrating sheet mask 1-2 times per week', 'duration': 15, 'products': ['Sheet Mask', 'Hydrating Mask']},
                    {'order': 2, 'step_name': 'Cream Mask', 'description': 'Apply creamy overnight mask for deep hydration', 'duration': 20, 'products': ['Sleep Mask', 'Hydrating Cream Mask']},
                ]
            },
            'combination': {
                'morning': [
                    {'order': 1, 'step_name': 'Gentle Cleanser', 'description': 'Use a gentle, balanced cleanser suitable for both dry and oily areas', 'duration': 2, 'products': ['Gentle Cleanser', 'Balancing Cleanser']},
                    {'order': 2, 'step_name': 'Toner', 'description': 'Use a balancing toner', 'duration': 2, 'products': ['Balancing Toner', 'pH Toner']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Apply lightweight, hydrating serum', 'duration': 2, 'products': ['Hydrating Serum', 'Lightweight Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Use lightweight, balanced moisturizer', 'duration': 2, 'products': ['Gel-Cream', 'Light Moisturizer']},
                    {'order': 5, 'step_name': 'Sunscreen', 'description': 'Apply SPF 30+ sunscreen', 'duration': 2, 'products': ['Sunscreen SPF 30+']},
                ],
                'evening': [
                    {'order': 1, 'step_name': 'Cleanser', 'description': 'Use gentle cleanser to remove makeup', 'duration': 3, 'products': ['Gentle Cleanser', 'Makeup Remover']},
                    {'order': 2, 'step_name': 'Toner', 'description': 'Apply balancing toner', 'duration': 2, 'products': ['Toner']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Apply lightweight serum or targeted treatment', 'duration': 3, 'products': ['Treatment Serum', 'Targeted Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Apply balanced night moisturizer', 'duration': 2, 'products': ['Night Cream', 'Moisturizer']},
                ],
                'weekly': [
                    {'order': 1, 'step_name': 'Gentle Exfoliant', 'description': 'Use gentle exfoliant 1 time per week', 'duration': 5, 'products': ['Gentle Exfoliant', 'Enzyme Exfoliant']},
                    {'order': 2, 'step_name': 'Balanced Mask', 'description': 'Apply balancing mask', 'duration': 12, 'products': ['Balancing Mask', 'Gel Mask']},
                ]
            },
            'sensitive': {
                'morning': [
                    {'order': 1, 'step_name': 'Gentle Cleanser', 'description': 'Use hypoallergenic, fragrance-free cleanser', 'duration': 2, 'products': ['Hypoallergenic Cleanser', 'Gentle Cleanser']},
                    {'order': 2, 'step_name': 'Calming Toner', 'description': 'Apply soothing toner with centella asiatica', 'duration': 2, 'products': ['Calming Toner', 'Centella Toner']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Use calming serum without active ingredients', 'duration': 2, 'products': ['Calming Serum', 'Soothing Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Apply hypoallergenic, fragrance-free moisturizer', 'duration': 2, 'products': ['Sensitive Moisturizer', 'Calming Cream']},
                    {'order': 5, 'step_name': 'Sunscreen', 'description': 'Apply mineral sunscreen SPF 30+', 'duration': 2, 'products': ['Mineral Sunscreen']},
                ],
                'evening': [
                    {'order': 1, 'step_name': 'Gentle Cleanser', 'description': 'Use gentle, hypoallergenic cleanser', 'duration': 3, 'products': ['Gentle Cleanser', 'Hypoallergenic Cleanser']},
                    {'order': 2, 'step_name': 'Calming Toner', 'description': 'Apply soothing toner', 'duration': 2, 'products': ['Calming Toner']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Apply soothing serum', 'duration': 3, 'products': ['Centella Serum', 'Calming Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Apply calming night cream', 'duration': 2, 'products': ['Sensitive Night Cream', 'Calming Cream']},
                ],
                'weekly': [
                    {'order': 1, 'step_name': 'Calming Mask', 'description': 'Use soothing sheet mask 1 time per week', 'duration': 15, 'products': ['Calming Sheet Mask', 'Soothing Mask']},
                ]
            },
            'normal': {
                'morning': [
                    {'order': 1, 'step_name': 'Cleanser', 'description': 'Use a gentle, daily cleanser', 'duration': 2, 'products': ['Daily Cleanser', 'Gentle Cleanser']},
                    {'order': 2, 'step_name': 'Toner', 'description': 'Apply toner to prep skin', 'duration': 2, 'products': ['Toner', 'Essence']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Use lightweight serum for added benefits', 'duration': 2, 'products': ['Vitamin C Serum', 'Light Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Apply daily moisturizer', 'duration': 2, 'products': ['Daily Moisturizer', 'Light Cream']},
                    {'order': 5, 'step_name': 'Sunscreen', 'description': 'Apply SPF 30+ sunscreen', 'duration': 2, 'products': ['Sunscreen SPF 30+']},
                ],
                'evening': [
                    {'order': 1, 'step_name': 'Cleanser', 'description': 'Use gentle cleanser to remove makeup', 'duration': 3, 'products': ['Makeup Remover', 'Cleanser']},
                    {'order': 2, 'step_name': 'Toner', 'description': 'Apply toner', 'duration': 2, 'products': ['Toner']},
                    {'order': 3, 'step_name': 'Serum', 'description': 'Apply targeted serum (retinol, peptide, etc)', 'duration': 3, 'products': ['Retinol Serum', 'Peptide Serum']},
                    {'order': 4, 'step_name': 'Moisturizer', 'description': 'Apply night moisturizer', 'duration': 2, 'products': ['Night Cream', 'Moisturizer']},
                ],
                'weekly': [
                    {'order': 1, 'step_name': 'Exfoliant', 'description': 'Use exfoliant 1-2 times per week', 'duration': 5, 'products': ['Exfoliant', 'Gentle Scrub']},
                    {'order': 2, 'step_name': 'Mask', 'description': 'Apply mask for added benefits', 'duration': 12, 'products': ['Face Mask', 'Sheet Mask']},
                ]
            }
        }
    
    def build_routine(self, skin_type: str, routine_type: str) -> SkincareRoutine:
        """Build a skincare routine based on skin type"""
        try:
            if skin_type not in self.routines:
                self.app_logger.warning(f"Unknown skin type: {skin_type}, using normal routine")
                skin_type = 'normal'
            
            routine_data = self.routines[skin_type].get(routine_type, [])
            
            steps = []
            total_duration = 0
            
            for step_data in routine_data:
                step = SkincareStep(
                    order=step_data['order'],
                    step_name=step_data['step_name'],
                    description=step_data['description'],
                    duration_minutes=step_data['duration'],
                    product_recommendations=step_data['products']
                )
                steps.append(step)
                total_duration += step_data['duration']
            
            routine = SkincareRoutine(
                routine_type=routine_type,
                steps=steps,
                total_duration_minutes=total_duration
            )
            
            self.app_logger.info(f"Built {routine_type} routine for {skin_type} skin type")
            return routine
        
        except Exception as e:
            self.app_logger.error(f"Error building routine: {str(e)}")
            raise
    
    def build_all_routines(self, skin_type: str) -> dict:
        """Build all routines (morning, evening, weekly) for a skin type"""
        return {
            'morning': self.build_routine(skin_type, 'morning'),
            'evening': self.build_routine(skin_type, 'evening'),
            'weekly': self.build_routine(skin_type, 'weekly'),
        }
