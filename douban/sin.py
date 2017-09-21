import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,2*np.pi,0.01)
y=np.sin(x)

plt.plot(x,y)
plt.xlabel("x轴")
plt.ylabel("y轴")
plt.title("sin函数")
plt.savefig("sin.jpg")

