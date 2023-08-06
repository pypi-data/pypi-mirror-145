"""This is ARTEMIS's alarm threshold policy library providing ready-made,
adaptable alarm threshold policies.
"""

def fixed(high_threshold, low_threshold):
    """Thresholds are set to fixed values."""
    def threshold_policy(patient, measurements, diagnoses, medications):
        return high_threshold, low_threshold
    
    threshold_policy.__name__ = f'fixed({high_threshold}, {low_threshold})'
    
    return threshold_policy

def offset(high_offset, low_offset):
    """Thresholds are set relative to the first measurement."""
    def threshold_policy(patient, measurements, diagnoses, medications):
        return measurements.iloc[0] + high_offset, measurements.iloc[0] - low_offset
    
    threshold_policy.__name__ = f'offset({high_offset}, {low_offset})'
    
    return threshold_policy