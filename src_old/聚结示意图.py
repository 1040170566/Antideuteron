import matplotlib.pyplot as plt
import numpy as np


# 1.圆半径
r = 2.0
# 2.圆心坐标
a, b = (0., 0.)
# ==========================================
# 方法一：参数方程
theta = np.arange(0, 2*np.pi, 0.01)
x = a + r * np.cos(theta)
y = b + r * np.sin(theta)
plt.figure()
plt.plot(x, y,'k')# 爱因斯坦环

the = 50
plt.annotate('', xytext=(-x[the],-y[the]), xy=(x[the],y[the]),
            arrowprops=dict(arrowstyle='<->', edgecolor='g'))
plt.text(-0.05, 0.1, '$p_{coal}$', rotation= theta[the]/np.pi*180)

p_pbar, p_nbar= [-1,0.5], [1, 0]
plt.scatter(p_pbar[0], p_pbar[1], c='b')
plt.scatter(0, 0.75, c='b')
plt.scatter(p_nbar[0], p_nbar[1], c='r')
plt.annotate('$\\bar{p}$', xy=p_pbar, xytext= [-2,1.5], arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.annotate('$\\bar{p}$', xy=[0, 0.75], xytext= [1.5,1.75], arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.annotate('$\\bar{n}$', xy=p_nbar, xytext= [2,-1.5], arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plt.axis('equal')
plt.axis('off')

plt.savefig(r'D:\学习资料\毕业论文\whu-graduation-thesis-latex\figures\coalescence sketch.png')
plt.savefig(r'D:\学习资料\毕业论文\whu-graduation-thesis-latex\figures\coalescence sketch.pdf')
plt.show()