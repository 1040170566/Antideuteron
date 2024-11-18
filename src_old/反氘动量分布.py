from 数据提取 import *

plt.figure('3.反氘的动量分布')

P_nu = [nu.P_value() for nu in antinucleon]
Pmax_nu, Pmin_nu = max(P_nu), min(P_nu)
# print(Pmax_nu, Pmin_nu)

bins_P_nu = np.linspace(Pmin_nu, Pmax_nu, bins_number + 1)

numbers_P_pbar, bins_P_nu = np.histogram(P_pbar, bins=bins_P_nu)
numbers_P_pbar = list(numbers_P_pbar)
for x in range(len(numbers_P_pbar)):
    numbers_P_pbar[x] /= (bins_P_nu[x + 1] - bins_P_nu[x]) * EventsNumber / np.sqrt(bins_P_nu[x] ** 2 + mass_pbar ** 2)
# plt.plot(bins_P_nu[:-1], numbers_P_pbar, label=r'$\bar{p}$')

numbers_P_nbar, bins_P_nu = np.histogram(P_nbar, bins=bins_P_nu)
numbers_P_nbar = list(numbers_P_nbar)
for x in range(len(numbers_P_nbar)):
    numbers_P_nbar[x] /= (bins_P_nu[x + 1] - bins_P_nu[x]) * EventsNumber / np.sqrt(bins_P_nu[x] ** 2 + mass_nbar ** 2)
# plt.plot(bins_P_nu[:-1], numbers_P_nbar, 'r', label=r'$\bar{n}$')

M_antideuteron = 1.875612928  # 反氘核质量
B_AP_A2 = M_antideuteron / mass_pbar / mass_nbar * Pcoal ** 3 * 2 / 3

numbers_P_antideuteron = []
bins_P_antideu = []
for x in range(bins_number):
    bins_P_antideu.append(2 * bins_P_nu[x])
    # numbers_P_antideuteron.append(B_AP_A2 * numbers_P_pbar[x] * numbers_P_nbar[x] / bins_P_antideu[x] ** 2)  #EdN/dp
    numbers_P_antideuteron.append(B_AP_A2 * numbers_P_pbar[x] * numbers_P_nbar[x] / bins_P_antideu[x] ** 2
                                  / np.sqrt(bins_P_antideu[x] ** 2 + M_antideuteron ** 2))  # dN/dp

plt.plot(bins_P_antideu, numbers_P_antideuteron, 'g', label=r'$\bar{D}$')

plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dp (/GeV/annihilation)')
plt.xlabel('p (GeV)')
plt.legend()
plt.title('反氘动量分布')
if lines == lines1:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反氘动量分布.png')
elif lines == lines2:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反氘动量分布.png')
# plt.show()

# 每一次事件产生反氘的个数
n_antideu = (bins_P_antideu[1] - bins_P_antideu[0]) * sum(numbers_P_antideuteron)
with open(r'D:\学习资料\毕业论文\模拟代码\每次事件产生的反氘数.txt', 'a', encoding='utf-8') as f:
    f.writelines([str(len(lines)), ' ', str(n_antideu), ' ', str(bins_number), ' \n'])
print(n_antideu)
