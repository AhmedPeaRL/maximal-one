import numpy as np
import json
from scipy import stats

def baseline(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.5,0.05)

def model(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.47,0.05)

N = 1000

baseline_scores=[]
model_scores=[]

for s in range(N):
    baseline_scores.append(baseline(s))
    model_scores.append(model(s))

baseline_scores=np.array(baseline_scores)
model_scores=np.array(model_scores)

improvement = baseline_scores.mean() - model_scores.mean()

t,p = stats.ttest_ind(baseline_scores,model_scores)

result={
"baseline_mean":float(baseline_scores.mean()),
"model_mean":float(model_scores.mean()),
"improvement":float(improvement),
"p_value":float(p),
"n":N
}

print(json.dumps(result,indent=2))

with open("artifacts/long_run.json","w") as f:
    json.dump(result,f,indent=2)
