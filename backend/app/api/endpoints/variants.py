from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.variant import VariantRequest, PredictionResponse, VariantsResponse
from app.core.alphagenome_client import AlphaGenomeClient
from app.dependencies import rate_limiter
from app.data.pharmaco_variants import PHARMACO_VARIANTS

router = APIRouter()
client = AlphaGenomeClient()

@router.get("/", response_model=VariantsResponse)
async def get_available_variants():
    """Get list of available pharmacogenomic variants"""
    return VariantsResponse(
        variants=list(PHARMACO_VARIANTS.keys()),
        total_count=len(PHARMACO_VARIANTS)
    )

@router.post("/predict", response_model=PredictionResponse)
async def predict_variant(
    request: VariantRequest,
    _: bool = Depends(rate_limiter)
):
    """
    Predict molecular effects of a pharmacogenomic variant
    """
    try:
        if request.variant_name not in PHARMACO_VARIANTS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Variant not found: {request.variant_name}. Available: {list(PHARMACO_VARIANTS.keys())}"
            )
        
        result = await client.predict_variant(request.variant_name)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
