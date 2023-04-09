from 数据提取 import *

plt.figure("反核子动能分布比较")
# 画出动能分数分布图

T_nu = [(nu.four_momentum[-1] - nu.mass) for nu in antinucleon]
Tmax_nu, Tmin_nu = max(T_nu), min(T_nu)
# print(Tmax_nu, Tmin_nu)
# bins_T_nu = np.linspace(Tmin_nu, Tmax_nu, bins_number + 1)  # 线性划分
bins_T_nu = nplog(Tmin_nu, Tmax_nu, bins_number + 1)  # 对数划分

numbers_T_nu, bins_T_nu = np.histogram(T_nu, bins=bins_T_nu)
numbers_T_nu = list(numbers_T_nu)
for ii in range(len(numbers_T_nu)):
    numbers_T_nu[ii] /= (bins_T_nu[ii + 1] - bins_T_nu[ii]) * EventsNumber
plt.plot(bins_T_nu[:-1], numbers_T_nu, label=r'$\bar{p}$')

# 读取老师的数据
with open(r"D:\学习资料\毕业论文\模拟代码\dnde_xx2ww_mx100GeV.txt", 'r', encoding='utf-8') as file:
    line= file.readlines()

T_of_Cai, dnde_pbar = [], []
for ii in range(1, len(line)):
    line[ii] = line[ii].split()
    T_of_Cai.append(float(line[ii][0]))
    dnde_pbar.append(float(line[ii][3])/2)

plt.plot(T_of_Cai, dnde_pbar, label='dnde_pbar_Cai')

# plt.xlim(1e-5, 1)
plt.ylim(1e-2, 10)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dT (/GeV/annihilation)')
plt.xlabel('$T(GeV)$')
plt.legend(loc = "upper left")
# if lines == lines1:
#     plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子动能分数分布.png')
# elif lines == lines2:
#     plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子动能分数分布.png')
plt.show()
