'''
x=反质子的动能/暗物质质量，计算dN/dlgx-lgx的分布
Time:2024.3
Author:WangXiao
'''


import madgraph数据提取 as mg
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#########################################
# 获取粒子动能以及x
T_nu = np.array([nu.four_momentum[-1] - nu.mass for nu in mg.antinucleon]) # 反核子动能
x_nu = T_nu/mg.M_DM # 动能分数
lgx_nu = np.log10(x_nu) # 动能分数的对数

bins_lgx = np.arange(-8.9, 0.01, 0.05)  # pppc4的bins
bins_lgx[-1] = 0

###########################################
# 统计
numbers_xT_nu = np.histogram(lgx_nu, bins=bins_lgx)[0].astype(float)
nor_dndlgx_nu = numbers_xT_nu / np.diff(bins_lgx) / mg.EventsNumber
nor_dndlgx_nu = np.append(nor_dndlgx_nu, 0)


if __name__ == '__main__':
    plt.scatter(10**bins_lgx, nor_dndlgx_nu, label=r'$\bar{p}$', s=5)

    # plt.xlim(1e-5, 1)
    # plt.ylim(1e-2, 10)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('dN/d$\\log{x}$')
    plt.xlabel('$x=K/M_{DM}$')
    plt.legend(loc = "upper left")
    plt.title(r'Kinetic fraction of $\bar{p}$($M_{DM}=$%d GeV)'%(round(mg.M_DM)))

    
    # 输出文件名
    name = f'dNdlgx_lgx_pbar_{mg.ChannelType}_{mg.M_DM}GeV_MG_{mg.EventsNumber:.1E}'

    # 图像存储
    plt.savefig(f'{mg.ResultOutputDir}/Figures/{name}.pdf')

    # 数据存储
    Data = np.array([[mg.M_DM]*len(bins_lgx), bins_lgx, nor_dndlgx_nu]).T
    Data2save = pd.DataFrame(Data, columns=['mDM', 'Log[10,x]', f'{mg.ChannelType}'])
    Data2save['mDM'] = Data2save['mDM'].astype(np.int64)
    # Data2save = Data2save[Data2save['T'] >=0.1]
    # print(Data2save)
    Data2save.to_csv(f'{mg.ResultOutputDir}/Data/{name}.dat', index=False, sep='\t')
