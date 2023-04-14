from 数据提取 import *

plt.figure('反质子反中子的动能分布')
# 画出动能分布图

T_pbar = [p.four_momentum[-1] - p.mass for p in pbar]
Tmax_pbar, Tmin_pbar = max(T_pbar), min(T_pbar)
# print(Tmax_pbar, Tmin_pbar)
bins_T_pbar = np.linspace(Tmin_pbar, Tmax_pbar, bins_number + 1)
# bins_T_pbar = nplog(Tmin_pbar, Tmax_pbar, bins_number + 1)

numbers_T_pbar, bins_T_pbar = np.histogram(T_pbar, bins=bins_T_pbar)
numbers_T_pbar = list(numbers_T_pbar)
for x in range(len(numbers_T_pbar)):
    numbers_T_pbar[x] /= (bins_T_pbar[x + 1] - bins_T_pbar[x]) * EventsNumber
plt.plot(bins_T_pbar[:-1], numbers_T_pbar, label=r'$\bar{p}$')
# plt.scatter(bins_T_pbar[:-1], numbers_T_pbar, s=2, label=r'$\bar{p}$')


T_nbar = [n.four_momentum[-1] - n.mass for n in nbar]
Tmax_nbar, Tmin_nbar = max(T_nbar), min(T_nbar)
# print(Emax_nbar, Emin_nbar)
bins_T_nbar = np.linspace(Tmin_nbar, Tmax_nbar, bins_number + 1)
# bins_T_nbar = nplog(Tmin_nbar, Tmax_nbar, bins_number + 1)

numbers_T_nbar, bins_T_nbar = np.histogram(T_nbar, bins=bins_T_nbar)
numbers_T_nbar = list(numbers_T_nbar)
for x in range(len(numbers_T_nbar)):
    numbers_T_nbar[x] /= (bins_T_nbar[x + 1] - bins_T_nbar[x]) * EventsNumber
plt.plot(bins_T_nbar[:-1], numbers_T_nbar, 'r', label=r'$\bar{n}$')
# plt.scatter(bins_T_nbar[:-1], numbers_T_nbar, s=2, c='r', label=r'$\bar{n}$')

plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dT (/GeV/annihilation)')
plt.xlabel('T (GeV)')
plt.legend()
plt.title('反质子反中子动能分布')
if lines == lines1:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子反中子动能分布.png')
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子反中子动能分布.eps', dpi= 300)
elif lines == lines2:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子反中子动能分布.png')
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子反中子动能分布.eps', dpi= 300)
plt.show()
