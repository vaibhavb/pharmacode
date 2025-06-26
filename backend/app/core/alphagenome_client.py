import os
import logging
from typing import Dict, Any
from app.models.variant import PredictionResponse, MolecularEffects, PredictionConfidence, RawData
from app.data.pharmaco_variants import PHARMACO_VARIANTS

# Mock AlphaGenome client for development
# Replace with actual AlphaGenome imports when API key is available
try:
    from alphagenome.data import genome
    from alphagenome.models import dna_client
    ALPHAGENOME_AVAILABLE = True
except ImportError:
    ALPHAGENOME_AVAILABLE = False
    logging.warning("AlphaGenome not available, using mock predictions")

class AlphaGenomeClient:
    def __init__(self):
        self.api_key = os.getenv('ALPHAGENOME_API_KEY')
        if ALPHAGENOME_AVAILABLE and self.api_key:
            self.model = dna_client.create(self.api_key)
        else:
            self.model = None
            logging.warning("Using mock AlphaGenome predictions")
    
    async def predict_variant(self, variant_name: str) -> PredictionResponse:
        if self.model and ALPHAGENOME_AVAILABLE:
            return await self._real_prediction(variant_name)
        else:
            return self._mock_prediction(variant_name)
    
    async def _real_prediction(self, variant_name: str) -> PredictionResponse:
        """Make real AlphaGenome prediction"""
        variant_info = PHARMACO_VARIANTS[variant_name]
        
        # Create genome interval
        interval = genome.Interval(
            chromosome=variant_info['chromosome'],
            start=variant_info['gene_region'][0],
            end=variant_info['gene_region'][1]
        )
        
        # Create variant object
        variant = genome.Variant(
            chromosome=variant_info['chromosome'],
            position=variant_info['position'],
            reference_bases=variant_info['ref'],
            alternate_bases=variant_info['alt']
        )
        
        # Request specific outputs
        requested_outputs = [
            dna_client.OutputType.RNA_SEQ,
            dna_client.OutputType.HISTONE_MARKS,
            dna_client.OutputType.TF_BINDING,
        ]
        
        # Make prediction
        outputs = self.model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=variant_info['ontology_terms'],
            requested_outputs=requested_outputs
        )
        
        return self._process_outputs(outputs, variant_name)
    
    def _mock_prediction(self, variant_name: str) -> PredictionResponse:
        """Generate mock predictions for development"""
        mock_data = {
            'CYP2D6*4': {
                'gene_expression_change': -45.2,
                'chromatin_accessibility_change': -20.1,
                'binding_sites_lost': 3,
                'binding_sites_gained': 0,
                'splicing_impact': 'Exon 3 exclusion'
            },
            'TPMT*3A_G460A': {
                'gene_expression_change': -35.5,
                'chromatin_accessibility_change': -15.2,
                'binding_sites_lost': 2,
                'binding_sites_gained': 1,
                'splicing_impact': 'Normal splicing'
            },
            'DPYD*2A': {
                'gene_expression_change': -55.0,
                'chromatin_accessibility_change': -30.5,
                'binding_sites_lost': 4,
                'binding_sites_gained': 0,
                'splicing_impact': 'Exon 14 skipping'
            },
            'UGT1A1*28': {
                'gene_expression_change': -30.0,
                'chromatin_accessibility_change': -12.0,
                'binding_sites_lost': 1,
                'binding_sites_gained': 0,
                'splicing_impact': 'Normal splicing'
            }
        }
        
        effects = mock_data.get(variant_name, mock_data['CYP2D6*4'])
        
        return PredictionResponse(
            variant_name=variant_name,
            molecular_effects=MolecularEffects(**effects),
            prediction_confidence=PredictionConfidence(
                expression="High" if abs(effects['gene_expression_change']) > 40 else "Medium",
                chromatin="Medium"
            ),
            raw_data=RawData(
                interval=f"chr1:1000000-1001000",
                reference_expression_profile=[1.0] * 100,
                alternate_expression_profile=[0.5] * 100
            )
        )
    
    def _process_outputs(self, outputs, variant_name: str) -> PredictionResponse:
        """Process real AlphaGenome outputs"""
        # Calculate gene expression change
        ref_expression = outputs.reference.rna_seq.values.mean()
        alt_expression = outputs.alternate.rna_seq.values.mean()
        expression_change = ((alt_expression - ref_expression) / ref_expression) * 100
        
        # Analyze histone marks
        ref_chromatin = outputs.reference.histone_marks.values.mean()
        alt_chromatin = outputs.alternate.histone_marks.values.mean()
        chromatin_change = ((alt_chromatin - ref_chromatin) / ref_chromatin) * 100
        
        # Find TF binding changes
        ref_tf_binding = outputs.reference.tf_binding.values.sum()
        alt_tf_binding = outputs.alternate.tf_binding.values.sum()
        tf_binding_change = alt_tf_binding - ref_tf_binding
        
        return PredictionResponse(
            variant_name=variant_name,
            molecular_effects=MolecularEffects(
                gene_expression_change=round(expression_change, 1),
                chromatin_accessibility_change=round(chromatin_change, 1),
                binding_sites_lost=max(0, -int(tf_binding_change)),
                binding_sites_gained=max(0, int(tf_binding_change)),
                splicing_impact=self._analyze_splicing(outputs)
            ),
            prediction_confidence=PredictionConfidence(
                expression=self._calculate_confidence(outputs.reference.rna_seq),
                chromatin=self._calculate_confidence(outputs.reference.histone_marks)
            ),
            raw_data=RawData(
                interval=str(outputs.reference.rna_seq.interval),
                reference_expression_profile=outputs.reference.rna_seq.values.tolist()[:100],
                alternate_expression_profile=outputs.alternate.rna_seq.values.tolist()[:100]
            )
        )
    
    def _analyze_splicing(self, outputs) -> str:
        """Analyze splicing impact"""
        ref_variance = outputs.reference.rna_seq.values.var()
        alt_variance = outputs.alternate.rna_seq.values.var()
        
        if abs(alt_variance - ref_variance) > ref_variance * 0.5:
            return "Significant splicing disruption detected"
        elif abs(alt_variance - ref_variance) > ref_variance * 0.2:
            return "Moderate splicing changes"
        else:
            return "Normal splicing pattern"
    
    def _calculate_confidence(self, prediction_data) -> str:
        """Calculate prediction confidence"""
        data_variance = prediction_data.values.var()
        if data_variance < 0.1:
            return "High"
        elif data_variance < 0.3:
            return "Medium" 
        else:
            return "Low"
