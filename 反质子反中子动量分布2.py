from 数据提取 import *
import 反质子反中子动量分布 as Mom

plt.figure("2.动量分布2 EdN/dp -p")

numbers2_P_pbar = Mom.numbers_P_pbar.copy()
for x in range(len(numbers2_P_pbar)):
    numbers2_P_pbar[x] *= np.sqrt(Mom.bins_P_pbar[x] ** 2 + mass_pbar ** 2)
# print(numbers2_P_pbar)
# plt.scatter(bins_P_pbar[:-1], numbers2_P_pbar, s=5, label=r'$\bar{p}$')
plt.plot(Mom.bins_P_pbar[:-1], numbers2_P_pbar, label=r'$\bar{p}$')

numbers2_P_nbar = Mom.numbers_P_nbar.copy()
for x in range(len(numbers2_P_nbar)):
    numbers2_P_nbar[x] *= np.sqrt(Mom.bins_P_nbar[x] ** 2 + mass_nbar ** 2)
# print(numbers_P_nbar)
# plt.scatter(bins_P_nbar[:-1], numbers_P_nbar, s=5, c='r', label=r'$\bar{n}$')
plt.plot(Mom.bins_P_nbar[:-1], numbers2_P_nbar, 'r', label=r'$\bar{n}$')

plt.xscale('log')
plt.yscale('log')
plt.ylabel('E dN/dp (/annihilation)')
plt.xlabel('p (GeV)')
plt.legend()
plt.title('反质子反中子动量分布(2)')
if lines == lines1:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子反中子动量分布(2).png')
elif lines == lines2:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子反中子动量分布(2).png')
plt.show()
