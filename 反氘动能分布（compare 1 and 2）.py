import matplotlib.pyplot as plt
import numpy as np

from 数据提取 import *
from 聚结条件 import antideuterons

plt.figure()

T_nu = [nu.four_momentum[-1] - nu.mass for nu in antinucleon]
Tmax_nu, Tmin_nu = max(T_nu), min(T_nu)
# print(Tmax_nu, Tmin_nu)

bins_T_nu = np.linspace(Tmin_nu, Tmax_nu, bins_number + 1)
# bins_T_nu = nplog(Tmin_nu, Tmax_nu, bins_number + 1)

T_pbar = [(p.four_momentum[-1] - p.mass) for p in pbar]
numbers_T_pbar, bins_T_nu = np.histogram(T_pbar, bins=bins_T_nu)
numbers_T_pbar = list(numbers_T_pbar)
for x in range(len(numbers_T_pbar)):
    numbers_T_pbar[x] /= (bins_T_nu[x + 1] - bins_T_nu[x]) * EventsNumber
# plt.plot(bins_T_nu[:-1], numbers_T_pbar, label=r'$\bar{p}$')

T_nbar = [(n.four_momentum[-1] - n.mass) for n in nbar]
numbers_T_nbar, bins_T_nu = np.histogram(T_nbar, bins=bins_T_nu)
numbers_T_nbar = list(numbers_T_nbar)
for x in range(len(numbers_T_nbar)):
    numbers_T_nbar[x] /= (bins_T_nu[x + 1] - bins_T_nu[x]) * EventsNumber
# plt.plot(bins_T_nu[:-1], numbers_T_nbar, 'r', label=r'$\bar{n}$')

B_AP_A = M_antideuteron / mass_pbar / mass_nbar * Pcoal ** 3 / 6

numbers_T_antideuteron = []
bins_P_antideu = []  # 反氘动量区间
bins_T_antideu = []  # 反氘动能区间

for x in range(bins_number):
    p_nu = np.sqrt((bins_T_nu[x] + mass_pbar) ** 2 - mass_pbar ** 2)  # 每核子动量
    bins_P_antideu.append(2 * p_nu)  # 反氘动量bins
    numbers_T_antideuteron.append(B_AP_A * numbers_T_pbar[x] * numbers_T_nbar[x] / bins_P_antideu[x])  # dN/dT

    bins_T_antideu.append(np.sqrt(bins_P_antideu[-1] ** 2 + M_antideuteron ** 2) - M_antideuteron)  # 反氘动能bins

plt.plot(bins_T_nu[:-1], numbers_T_antideuteron, 'g', label='方法1')



vecP_Dbar = [d[1] + d[0] for d in antideuterons]
P_Dbar = [computeDistance(dd, [0, 0, 0]) for dd in vecP_Dbar]
T_Dbar = [np.sqrt(p * p + M_antideuteron ** 2) - M_antideuteron for p in P_Dbar]
Tmax_D, Tmin_D = max(T_Dbar), min(T_Dbar)

bins_T_D = np.linspace(Tmin_D, Tmax_D, 150 + 1)
# bins_T_D = nplog(Tmin_D, Tmax_D, bins_number + 1)
numbers_T_D, bins_T_D = np.histogram(T_Dbar, bins=bins_T_D)
numbers_T_D = list(numbers_T_D)
for x in range(len(numbers_T_D)):
    numbers_T_D[x] /= (bins_T_D[x + 1] - bins_T_D[x]) * EventsNumber

bins_T_Deverynu = [EveryNu / 2 for EveryNu in bins_T_D]

plt.scatter(bins_T_Deverynu[:-1], numbers_T_D, label= '方法2', color='grey', s=10, marker='D')
# plt.plot(bins_T_Deverynu[:-1], numbers_T_D, label= '方法2', color='grey', marker='D')


plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dT (/GeV/annihilation)')
plt.xlabel('T (GeV/nucleon)')
plt.legend(loc='center')
plt.show()

# plt.savefig(r'D:\学习资料\毕业论文\whu-graduation-thesis-latex\figures\compare.png')
plt.savefig(r'D:\学习资料\毕业论文\whu-graduation-thesis-latex\figures\compare.pdf')
