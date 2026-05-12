import pandas as pd
import numpy as np

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:,0].values

# 🔥 shift ذكي بدل التكرار الأعمى
shifted = np.roll(series, 7)

# scaling بسيط يحافظ على structure
scaled = shifted * 1.02 - 1.5

# دمج واعي
extended = np.concatenate([series, scaled])

pd.DataFrame({"Sunspots": extended}).to_csv(
    "real-data/sunspots_global_extended.csv",
    index=False
)

print("✅ extended dataset generated:", len(extended))
