from 数据提取 import *
from 反氘动能分布 import bins_T_antideu, numbers_T_antideuteron

plt.figure("反氘动能分数分布")

bins_xT_antideu = [t/M_DM for t in bins_T_antideu]
numbers_xT_antideuteron = []
for ii in range(len(bins_xT_antideu)):
    numbers_xT_antideuteron.append(numbers_T_antideuteron[ii]*bins_T_antideu[ii]*np.log(10))
plt.plot(bins_xT_antideu, numbers_xT_antideuteron, 'g', label=r'$\bar{D}$')

# plt.xlim(1e-5, 1)
# plt.ylim(1e-7, 1e-4)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/d$\\log{x}$ (/annihilation)')
plt.xlabel('$x=K/M_{DM}$')
plt.legend()
plt.title('反氘动能分数x分布（$M_{DM}=$%d GeV）'%(round(M_DM)))
if lines == lines1:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\反氘动能分数分布.png')
elif lines == lines2:
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events.hepmc(2)\反氘动能分数分布.png')
plt.show()
