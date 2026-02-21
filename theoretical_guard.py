def verify_monotonic_decrease(history, tolerance=1e-8):
    return (history <= tolerance).all()

def bounded_input_check(perturbations, M):
    import numpy as np
    return np.max(np.linalg.norm(perturbations, axis=1)) <= M
