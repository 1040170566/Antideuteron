'''
Target: 统计数据中的反质子（包括反中子）动能分布
Time: 2024.3
Author: WangXiao
'''

import madgraph数据提取 as mg
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

###################################################################
# 确定动能区间
T_nu = [nu.four_momentum[-1] - nu.mass for nu in mg.antinucleon]
Tmax_nu, Tmin_nu = max(T_nu), min(T_nu)

# bins_T_nu = np.linspace(Tmin_nu, Tmax_nu, mg.bins_number + 1)
bins_T_nu = mg.nplog(Tmin_nu, Tmax_nu, mg.bins_number + 1)

###################################################################
# 反核子动能分布
numbers_T_nu = np.histogram(T_nu, bins=bins_T_nu)[0].astype(float)
nor_dndT_nu = numbers_T_nu / np.diff(bins_T_nu) / mg.EventsNumber
nor_dndT_nu = np.append(nor_dndT_nu, 0)


if __name__ == '__main__':
    # plt.plot(bins_T_nu, nor_dndT_nu, 'g', label=r'$\bar{p}$')
    plt.scatter(bins_T_nu, nor_dndT_nu, label=r'$\bar{p}$', s=5)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('dN/dT (/GeV/annihilation)')
    plt.xlabel('T (GeV)')
    plt.legend()
    plt.title(r'Kinetic Energy Distribution of $\bar{p}$')
    # plt.show()

    # 输出文件名
    name = f'dNdT_T_pbar_{mg.ChannelType}_{mg.M_DM}GeV_MG_{mg.EventsNumber:.1E}'

    # 图像存储
    plt.savefig(f'{mg.ResultOutputDir}/图/{name}.pdf')

    # 数据存储
    DATA = np.array([bins_T_nu, nor_dndT_nu]).T
    Data2save = pd.DataFrame(DATA, columns=['T', 'dN/dT'])
    Data2save = Data2save[Data2save['T'] >=0.1]
    # print(Data2save)
    Data2save.to_csv(f'{mg.ResultOutputDir}/数据/{name}.dat', index=False, sep='\t')
