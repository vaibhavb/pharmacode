# Pharmacogenomic variant definitions for PharmaCode

PHARMACO_VARIANTS = {
    'CYP2D6*4': {
        'chromosome': 'chr22',
        'position': 42522500,
        'ref': 'G',
        'alt': 'A',
        'gene_region': (42522000, 42523000),
        'ontology_terms': ['liver', 'hepatocyte'],
        'description': 'Splice site variant causing reduced enzyme activity',
        'clinical_significance': 'Poor metabolizer',
        'affected_drugs': ['Codeine', 'Tramadol', 'Dextromethorphan']
    },
    'TPMT*3A_G460A': {
        'chromosome': 'chr6', 
        'position': 18138997,
        'ref': 'G',
        'alt': 'A',
        'gene_region': (18138500, 18139500),
        'ontology_terms': ['hematopoietic system'],
        'description': 'Dual variants causing enzyme instability',
        'clinical_significance': 'Poor metabolizer',
        'affected_drugs': ['6-Mercaptopurine', 'Azathioprine', '6-Thioguanine']
    },
    'DPYD*2A': {
        'chromosome': 'chr1',
        'position': 97915614, 
        'ref': 'G',
        'alt': 'A',
        'gene_region': (97915000, 97916000),
        'ontology_terms': ['liver', 'small intestine'],
        'description': 'Splice donor variant causing skipped exon',
        'clinical_significance': 'Poor metabolizer',
        'affected_drugs': ['5-Fluorouracil', 'Capecitabine', 'Tegafur']
    },
    'UGT1A1*28': {
        'chromosome': 'chr2',
        'position': 234668879,
        'ref': 'A',
        'alt': 'TA',
        'gene_region': (234668000, 234669000),
        'ontology_terms': ['liver'],
        'description': 'Promoter variant reducing transcription',
        'clinical_significance': 'Intermediate metabolizer',
        'affected_drugs': ['Irinotecan', 'Bilirubin']
    }
}
