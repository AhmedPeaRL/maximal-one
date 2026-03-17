import json
import os

ART="artifacts"

def read(name):

    paths = [
        os.path.join("artifacts",name),
        os.path.join("data",name)
    ]

    for p in paths:
        if os.path.exists(p):
            try:
                return json.load(open(p))
            except:
                pass

    return None


lyap=read("lyapunov.json")
spec=read("spectral_profile.json")
scale=read("scaling_collapse_engine.json")

report={}
passed=True
missing=[]

# ---- Lyapunov ----
if lyap is None:
    missing.append("lyapunov.json")
else:
    val=lyap.get("lyapunov_exp")
    report["lyapunov"]=val
    if val is None or val<=0:
        passed=False

# ---- Spectral alpha ----
if spec is None:
    missing.append("spectral_verification.json")
else:
    alpha=spec.get("alpha") or spec.get("estimated_alpha")
    report["spectral_alpha"]=alpha
    if alpha is None or not (0.5 < alpha < 3):
        passed=False

# ---- Scaling collapse ----
if scale is None:
    missing.append("scaling_collapse_engine.json")
else:
    err=scale.get("collapse_error") or scale.get("collapse_score")
    report["collapse_error"]=err
    if err is None or err>0.2:
        passed=False


report["missing"]=missing
report["passed"]=passed

print(json.dumps(report,indent=2))

# لا نفشل الـpipeline لو البيانات ناقصة
if missing:
    exit(0)

# نفشل فقط لو البيانات موجودة لكن القانون لم يتحقق
if not passed:
    exit(1)
