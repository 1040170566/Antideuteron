from 数据提取 import *

Pmax_pbar, Pmin_pbar = max(P_pbar), min(P_pbar)  # 反质子动量最值
# print(Pmax_pbar, Pmin_pbar)
Pmax_nbar, Pmin_nbar = max(P_nbar), min(P_nbar)  # 反中子动量最值
# print(Pmax_nbar, Pmin_nbar)

plt.figure("1.动量分布dN/dp -p")

bins_P_pbar = np.linspace(Pmin_pbar, Pmax_pbar, bins_number + 1)
numbers_P_pbar, bins_P_pbar = np.histogram(P_pbar, bins=bins_P_pbar)
numbers_P_pbar = list(numbers_P_pbar)
for x in range(len(numbers_P_pbar)):
    numbers_P_pbar[x] /= (bins_P_pbar[x + 1] - bins_P_pbar[x]) * EventsNumber
# print(numbers_P_pbar)
# plt.scatter(bins_P_pbar[:-1], numbers_P_pbar, s=5, label=r'$\bar{p}$')
plt.plot(bins_P_pbar[:-1], numbers_P_pbar, label=r'$\bar{p}$')


bins_P_nbar = np.linspace(Pmin_nbar, Pmax_nbar, bins_number + 1)
numbers_P_nbar, bins_P_nbar = np.histogram(P_nbar, bins=bins_P_nbar)
numbers_P_nbar = list(numbers_P_nbar)
for x in range(len(numbers_P_nbar)):
    numbers_P_nbar[x] /= (bins_P_nbar[x + 1] - bins_P_nbar[x]) * EventsNumber
# print(numbers_P_nbar)
# plt.scatter(bins_P_nbar[:-1], numbers_P_nbar, s=5, c='r', label=r'$\bar{n}$')
plt.plot(bins_P_nbar[:-1], numbers_P_nbar, 'r', label=r'$\bar{n}$')

plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dp (/GeV/annihilation)')
plt.xlabel('p (GeV)')
plt.legend()
plt.title('反质子反中子动量分布')
if lines == lines1:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子反中子动量分布.png')
elif lines == lines2:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子反中子动量分布.png')
plt.show()
