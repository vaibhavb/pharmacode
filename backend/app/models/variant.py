from pydantic import BaseModel
from typing import List, Optional

class VariantRequest(BaseModel):
    variant_name: str

class MolecularEffects(BaseModel):
    gene_expression_change: float
    chromatin_accessibility_change: float
    binding_sites_lost: int
    binding_sites_gained: int
    splicing_impact: str

class PredictionConfidence(BaseModel):
    expression: str
    chromatin: str

class RawData(BaseModel):
    interval: str
    reference_expression_profile: List[float]
    alternate_expression_profile: List[float]

class PredictionResponse(BaseModel):
    variant_name: str
    molecular_effects: MolecularEffects
    prediction_confidence: PredictionConfidence
    raw_data: RawData

class VariantsResponse(BaseModel):
    variants: List[str]
    total_count: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
