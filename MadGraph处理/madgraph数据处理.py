import madgraph数据提取 as mg
import numpy as np
import matplotlib.pyplot as plt

T_nu = [nu.four_momentum[-1] - nu.mass for nu in mg.antinucleon]
Tmax_nu, Tmin_nu = max(T_nu), min(T_nu)

# bins_T_nu = np.linspace(Tmin_nu, Tmax_nu, mg.bins_number + 1)
bins_T_nu = mg.nplog(Tmin_nu, Tmax_nu, mg.bins_number + 1)

# 反质子动能归一化分布
T_pbar = [(p.four_momentum[-1] - p.mass) for p in mg.pbar]
numbers_T_pbar = np.histogram(T_pbar, bins=bins_T_nu)[0].astype(float)
nor_dndT_pbar = numbers_T_pbar / np.diff(bins_T_nu) / mg.EventsNumber

# 反中子动能归一化分布
T_nbar = [(n.four_momentum[-1] - n.mass) for n in mg.nbar]
numbers_T_nbar = np.histogram(T_nbar, bins=bins_T_nu)[0].astype(float)
nor_dndT_nbar = numbers_T_nbar / np.diff(bins_T_nu) / mg.EventsNumber

# 聚结参数 * 反氘动量
B_AP_A = mg.M_antideuteron / mg.mass_pbar / mg.mass_nbar * mg.Pcoal ** 3 / 6

bins_p_nu = np.sqrt((bins_T_nu + mg.mass_pbar) ** 2 - mg.mass_pbar ** 2)  # 每核子动量
bins_p_antideu = bins_p_nu * 2  # 反氘动量bins
nor_dndT_antideuteron = B_AP_A / bins_p_antideu[:-1] * nor_dndT_pbar * nor_dndT_nbar  # 反氘动能归一化分布
bins_T_antideu = np.sqrt(bins_p_antideu ** 2 + mg.M_antideuteron ** 2) - mg.M_antideuteron  # 反氘动能bins


if __name__ == '__main__':
    plt.plot(bins_T_antideu[:-1], nor_dndT_antideuteron, 'g', label=r'$\bar{D}$')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('dN/dT (/GeV/annihilation)')
    plt.xlabel('T (GeV)')
    # plt.legend()
    # plt.title('反氘动能分布')
    # plt.savefig(r'/home/wangxiao/文档/ee2bb_MG.pdf')
    #
    # DATA = np.array([bins_T_antideu, numbers_T_antideuteron])
    # np.savetxt(r'/home/wangxiao/文档/dndt_t_bb_MG.dat', DATA)
    plt.show()
