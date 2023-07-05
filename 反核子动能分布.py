import matplotlib.pyplot as plt
import numpy as np

from madgraph数据提取 import *

plt.figure("反核子动能分布")
# 画出动能分数分布图

T_nu = [(nu.four_momentum[-1] - nu.mass) for nu in antinucleon]
Tmax_nu, Tmin_nu = max(T_nu), min(T_nu)
# bins_T_nu = np.linspace(Tmin_nu, Tmax_nu, bins_number + 1)
bins_T_nu = nplog(Tmin_nu, Tmax_nu, bins_number + 1)

numbers_T_nu, bins_T_nu = np.histogram(T_nu, bins=bins_T_nu)
numbers_T_nu = list(numbers_T_nu)
for ii in range(len(numbers_T_nu)):
    numbers_T_nu[ii] /= (bins_T_nu[ii + 1] - bins_T_nu[ii]) * EventsNumber
plt.plot(bins_T_nu[:-1], numbers_T_nu, label=r'$\bar{p}$')

# plt.xlim(1e-5, 1)
# plt.ylim(1e-2, 10)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dT (/annihilation)')
plt.xlabel('T')
plt.legend(loc = "upper left")
plt.title('antiproton')
plt.savefig(r"/home/wangxiao/文档/ee2bb_antip_MG.pdf")
# plt.show()

DATA = np.array([bins_T_nu[:-1],numbers_T_nu])
np.savetxt(r"/home/wangxiao/文档/dndt_t_bb_antip_MG.dat", DATA)
