from madgraph数据提取 import *

T_nu = [nu.four_momentum[-1] - nu.mass for nu in antinucleon]
Tmax_nu, Tmin_nu = max(T_nu), min(T_nu)
# print(Tmax_nu, Tmin_nu)

#bins_T_nu = np.linspace(Tmin_nu, Tmax_nu, bins_number + 1)
bins_T_nu = nplog(Tmin_nu, Tmax_nu, bins_number + 1)

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

    bins_T_antideu.append(np.sqrt(bins_P_antideu[-1]**2+M_antideuteron**2)-M_antideuteron)  # 反氘动能bins

plt.plot(bins_T_antideu, numbers_T_antideuteron, 'g', label=r'$\bar{D}$')

plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dT (/GeV/annihilation)')
plt.xlabel('T (GeV)')
# plt.legend()
# plt.title('反氘动能分布')
plt.savefig(r'/home/wangxiao/文档/ee2bb_MG.pdf')


DATA = np.array([bins_T_antideu, numbers_T_antideuteron])
np.savetxt(r'/home/wangxiao/文档/dndt_t_bb_MG.dat', DATA)
