import matplotlib.pyplot as plt
import numpy as np

from 数据提取 import *

plt.figure("反核子动能分数分布")
# 画出动能分数分布图

xT_nu = [(nu.four_momentum[-1] - nu.mass) / M_DM for nu in antinucleon]
xTmax_nu, xTmin_nu = max(xT_nu), min(xT_nu)
# print(xTmax_nu, xTmin_nu)
# bins_xT_nu = np.linspace(xTmin_nu, xTmax_nu, bins_number + 1)
bins_xT_nu = nplog(xTmin_nu, xTmax_nu, bins_number + 1)

numbers_xT_nu, bins_xT_nu = np.histogram(xT_nu, bins=bins_xT_nu)
numbers_xT_nu = list(numbers_xT_nu)
for ii in range(len(numbers_xT_nu)):
    numbers_xT_nu[ii] /= (bins_xT_nu[ii + 1] - bins_xT_nu[ii]) / bins_xT_nu[ii] / np.log(10) * EventsNumber
plt.plot(bins_xT_nu[:-1], numbers_xT_nu, label=r'$\bar{p}$')

plt.xlim(1e-5, 1)
plt.ylim(1e-2, 10)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/d$\\log{x}$ (/annihilation)')
plt.xlabel('$x=K/M_{DM}$')
plt.legend(loc = "upper left")
plt.title('反质子动能分数x分布（$M_{DM}=$%d GeV）'%(round(M_DM)))
if lines == lines1:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子动能分数分布.png')
elif lines == lines2:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子动能分数分布.png')
plt.show()
