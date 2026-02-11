from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class SkinToneEnum(str, Enum):
    FAIR = "fair"
    LIGHT = "light"
    MEDIUM = "medium"
    OLIVE = "olive"
    DEEP = "deep"
    DARK = "dark"

class UndertoneEnum(str, Enum):
    WARM_GOLDEN = "warm_golden"
    WARM_OLIVE = "warm_olive"
    COOL = "cool"
    NEUTRAL = "neutral"

class SeasonEnum(str, Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"
    WINTER = "Winter"

class SkinTypeEnum(str, Enum):
    OILY = "oily"
    DRY = "dry"
    COMBINATION = "combination"
    SENSITIVE = "sensitive"
    NORMAL = "normal"

class AnalysisRequest(BaseModel):
    """Request model for image analysis"""
    image_data: str = Field(..., description="Base64 encoded image data")
    gender: Optional[str] = Field(None, description="User gender (optional for better recommendations)")

class SkinAnalysisResponse(BaseModel):
    """Response model for skin analysis results"""
    skin_tone_rgb: dict = Field(..., description="RGB values of skin tone")
    skin_tone_hex: str = Field(..., description="Hex color code of skin tone")
    skin_tone_hsv: dict = Field(..., description="HSV values of skin tone")
    undertone: UndertoneEnum = Field(..., description="Classified undertone")
    season: SeasonEnum = Field(..., description="Seasonal color type")
    skin_type: SkinTypeEnum = Field(..., description="Classified skin type")
    confidence_scores: dict = Field(..., description="Confidence scores for classifications")

class ProductRecommendation(BaseModel):
    """Product recommendation details"""
    name: str = Field(..., description="Product name")
    brand: str = Field(..., description="Brand name")
    category: str = Field(..., description="Product category")
    shade: str = Field(..., description="Product shade")
    price_inr: float = Field(..., description="Price in INR")
    image_url: str = Field(..., description="Product image URL")
    rating: float = Field(..., description="Product rating (0-5)")
    reviews_count: int = Field(..., description="Number of reviews")
    buy_link: str = Field(..., description="Direct purchase link")
    delta_e_distance: Optional[float] = Field(None, description="Color matching distance")

class SkincareStep(BaseModel):
    """Single skincare routine step"""
    order: int = Field(..., description="Step order")
    step_name: str = Field(..., description="Name of the step")
    description: str = Field(..., description="Detailed description")
    duration_minutes: int = Field(..., description="Duration in minutes")
    product_recommendations: List[str] = Field(default_factory=list, description="Product suggestions")

class SkincareRoutine(BaseModel):
    """Complete skincare routine"""
    routine_type: str = Field(..., description="Type of routine (morning, evening, or weekly)")
    steps: List[SkincareStep] = Field(..., description="List of routine steps")
    total_duration_minutes: int = Field(..., description="Total routine duration")

class AnalysisResultsResponse(BaseModel):
    """Complete analysis results with recommendations"""
    skin_analysis: SkinAnalysisResponse = Field(..., description="Skin analysis results")
    foundation_recommendations: List[ProductRecommendation] = Field(..., description="Top 5 foundation options")
    blush_recommendations: List[ProductRecommendation] = Field(..., description="Top 5 blush options")
    lipstick_recommendations: List[ProductRecommendation] = Field(..., description="Top 5 lipstick options")
    concealer_recommendations: List[ProductRecommendation] = Field(..., description="Top 5 concealer options")
    eyeshadow_recommendations: List[ProductRecommendation] = Field(..., description="Top 5 eyeshadow options")
    morning_routine: SkincareRoutine = Field(..., description="Morning skincare routine")
    evening_routine: SkincareRoutine = Field(..., description="Evening skincare routine")
    weekly_routine: SkincareRoutine = Field(..., description="Weekly skincare routine")
    analysis_timestamp: str = Field(..., description="Timestamp of analysis")

class HealthResponse(BaseModel):
    """API health check response"""
    status: str = Field("ok", description="API status")
    version: str = Field(..., description="API version")
    message: str = Field("API is running", description="Status message")
