THRESHOLD_VARIANCE = 0.06

def is_stable(variance):
    return variance <= THRESHOLD_VARIANCE
