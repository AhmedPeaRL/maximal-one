import numpy as np
import pandas as pd

sigma=10
rho=28
beta=8/3

dt=0.01
steps=10000

x,y,z=1.0,1.0,1.0
data=[]

for i in range(steps):
    dx=sigma*(y-x)
    dy=x*(rho-z)-y
    dz=x*y-beta*z

    x+=dx*dt
    y+=dy*dt
    z+=dz*dt

    data.append([i*dt,x])

df=pd.DataFrame(data,columns=["t","x"])
df.to_csv("real-data/lorenz63.csv",index=False)
