from 数据提取 import *

plt.figure("4.动能分数分布")
# 画出动能分布图
x_T_pbar = [(p.four_momentum[-1] - p.mass) / M_DM for p in pbar]
x_Tmax_pbar, x_Tmin_pbar = max(x_T_pbar), min(x_T_pbar)
# print(x_Tmax_pbar, x_Tmin_pbar)
# bins_xT_pbar = np.linspace(x_Tmin_pbar, x_Tmax_pbar, bins_number + 1)
bins_xT_pbar = nplog(x_Tmin_pbar, x_Tmax_pbar, bins_number + 1)

numbers_xT_pbar, bins_xT_pbar = np.histogram(x_T_pbar, bins=bins_xT_pbar)
numbers_xT_pbar = list(numbers_xT_pbar)
for ii in range(len(numbers_xT_pbar)):
    numbers_xT_pbar[ii] /= (bins_xT_pbar[ii + 1] - bins_xT_pbar[ii]) / bins_xT_pbar[ii]/np.log(10) * EventsNumber
# plt.scatter(bins_xT_pbar[:-1], numbers_xT_pbar, s=5, label=r'$\bar{p}$')
plt.plot(bins_xT_pbar[:-1], numbers_xT_pbar, label=r'$\bar{p}$')

x_T_nbar = [(n.four_momentum[-1] - n.mass) / M_DM for n in nbar]
x_Tmax_nbar, x_Tmin_nbar = max(x_T_nbar), min(x_T_nbar)
# print(x_Tmax_nbar, x_Tmin_nbar)
# bins_xT_nbar = np.linspace(x_Tmin_nbar, x_Tmax_nbar, bins_number + 1)
bins_xT_nbar = nplog(x_Tmin_nbar, x_Tmax_nbar, bins_number + 1)

numbers_xT_nbar, bins_xT_nbar = np.histogram(x_T_nbar, bins=bins_xT_nbar)
numbers_xT_nbar = list(numbers_xT_nbar)
for ii in range(len(numbers_xT_nbar)):
    numbers_xT_nbar[ii] /= (bins_xT_nbar[ii + 1] - bins_xT_nbar[ii]) / bins_xT_nbar[ii]/np.log(10) * EventsNumber
# plt.scatter(bins_xT_nbar[:-1], numbers_xT_nbar, s=5, c='r', label=r'$\bar{n}$')
plt.plot(bins_xT_nbar[:-1], numbers_xT_nbar, 'r', label=r'$\bar{n}$')

# plt.ylim(0,1)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/d$\\log{x}$ (/annihilation)')
plt.xlabel('$x=K/M_{DM}$')
plt.legend(loc = "upper left")
plt.title('反质子反中子动能分数x分布（$M_{DM}=$%d GeV）'%(round(M_DM)))
# if lines == lines1:
#     plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反质子反中子动能分数分布.png')
# elif lines == lines2:
#     plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反质子反中子动能分数分布.png')
plt.show()
