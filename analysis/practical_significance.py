import numpy as np

mse_naive = 0.16315098709199394
mse_hcm = 0.16304039526657493

effect = (mse_naive - mse_hcm) / mse_naive

print("Relative improvement:", effect)

if effect < 0.01:
    raise SystemExit("Improvement not practically meaningful")
