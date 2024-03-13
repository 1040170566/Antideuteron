from 数据提取 import *

plt.figure("光子能量比较")
# 画出能量分布图

E_gamma = [ga.four_momentum[-1] for ga in gamma]
Emax_gamma, Emin_gamma = max(E_gamma), min(E_gamma)
# print(Emax_gamma, Emin_gamma)
# bins_E_gama = np.linspace(Emin_gamma, Emax_gamma, bins_number + 1)  # 线性划分
bins_E_gama = nplog(Emin_gamma, Emax_gamma, bins_number + 1)  # 对数划分

numbers_E_Gamma, bins_E_gama = np.histogram(E_gamma, bins=bins_E_gama)
numbers_E_Gamma = list(numbers_E_Gamma)
for ii in range(len(numbers_E_Gamma)):
    numbers_E_Gamma[ii] /= (bins_E_gama[ii + 1] - bins_E_gama[ii]) * EventsNumber
plt.plot(bins_E_gama[:-1], numbers_E_Gamma, label=r'$\gamma$')


# 读取老师的数据
with open(r"D:\学习资料\毕业论文\模拟代码\dnde_xx2ww_mx100GeV.txt", 'r', encoding='utf-8') as file:
    line= file.readlines()

T_of_Cai = []
dnde_gamma = []
for ii in range(1, len(line)):
    line[ii] = line[ii].split()
    T_of_Cai.append(float(line[ii][0]))
    dnde_gamma.append(float(line[ii][1])/2)

plt.plot(T_of_Cai, dnde_gamma, label='dnde_gamma_Cai')

plt.xlim(1e-7, 50)
plt.ylim(1e-4, 1e3)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dE (/GeV/annihilation)')
plt.xlabel('$E(GeV)$')
plt.legend(loc = "lower center")
# if lines == lines1:
#     plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子动能分数分布.png')
# elif lines == lines2:
#     plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子动能分数分布.png')
plt.show()
