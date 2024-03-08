"""
相比'madgraph数据处理.py'，此版先给定bins
"""

import madgraph数据提取 as mg
import numpy as np
# import matplotlib.pyplot as plt

bins_lgx = np.arange(-8.9, 0.01, 0.05)  # pppc4的bins
bins_lgx[-1] = 0
bins_x = 10 ** bins_lgx  # x=反氘动能/暗物质质量
bins_T_antideu = bins_x * mg.M_DM  # 反氘动能bins
bins_p_antideu = np.sqrt((bins_T_antideu + mg.M_antideuteron) ** 2 - mg.M_antideuteron ** 2)  # 反氘动量bins
bins_p_nu = bins_p_antideu / 2  # 每核子动量
bins_T_nu = np.sqrt(bins_p_nu ** 2 + mg.mass_pbar ** 2) - mg.mass_pbar  # 每核子动能区间，假定质子中子质量相同

# 反质子动能归一化分布
T_pbar = [(p.four_momentum[-1] - p.mass) for p in mg.pbar]
numbers_T_pbar = np.histogram(T_pbar, bins=bins_T_nu)[0].astype(float)
nor_dndT_pbar = numbers_T_pbar / np.diff(bins_T_nu) / mg.EventsNumber

# 反中子动能归一化分布
T_nbar = [(n.four_momentum[-1] - n.mass) for n in mg.nbar]
numbers_T_nbar = np.histogram(T_nbar, bins=bins_T_nu)[0].astype(float)
nor_dndT_nbar = numbers_T_nbar / np.diff(bins_T_nu) / mg.EventsNumber

B_AP_A = mg.M_antideuteron / mg.mass_pbar / mg.mass_nbar * mg.Pcoal ** 3 / 6  # 聚结参数 * 反氘动量
nor_dndT_antideuteron = B_AP_A / bins_p_antideu[:-1] * nor_dndT_pbar * nor_dndT_nbar  # 反氘动能归一化分布
# 在最后添加一个0，使得len(bins_lgx) = len(nor_dndT_antideuteron) + 1
nor_dndT_antideuteron = np.append(nor_dndT_antideuteron, 0)
# TODO:反氘能谱的计算，公式采用simplied coalescence model，结果与pppc4差距比较大。

dNdlgx_antideuteron = nor_dndT_antideuteron * bins_T_antideu * np.log(10)  # dN/dlgx

if __name__ == '__main__':
    # plt.plot(bins_x, dNdlgx_antideuteron, 'g', label=r'$\bar{D}$')
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.xlim([1e-5, 1])
    # plt.ylim([1e-7, 1e-3])
    # plt.ylabel('dN/dlgx (/GeV/annihilation)')
    # plt.xlabel('x')
    # plt.legend()
    # plt.title('反氘动能分布')
    # plt.savefig(fr'{mg.ResultOutputDir}/图/dNdlgx_x_antideu_{mg.ChannelType}_{mg.M_DM}GeV_MG.pdf')
    # plt.show()

    # 数据保存为.dat，方便后续处理读取，不用重新计算
    DATA = np.array([bins_x, dNdlgx_antideuteron])
    with open(f'{mg.ResultOutputDir}/dNdlgx_x_antideu_{mg.ChannelType}_{mg.M_DM}GeV_MG_{mg.EventsNumber:.1E}', 'w') as f:
        f.write('x=T/M_DM' + '\t\t\t\t ' 'dN/dlgx\n')
        np.savetxt(f, DATA.T)
