# 提取pppc4的数据
import pandas as pd
from matplotlib import pyplot as plt


def read_pppc4(DATA):
    print('首行数据为：')
    name = DATA.columns.tolist()
    for n in range(len(name)):
        print(f'{n}.{name[n]}')
    column_select = int(input('你的选择：'))
    # column_select = 13 # bb

    energy_set = DATA.mDM.unique()
    print('记录的能量为：')
    for n in range(len(energy_set)):
        print(f'{n}.{energy_set[n]}')
    energy_number = int(input('需要观察的能量：'))
    # energy_number = 11
    energy = energy_set[energy_number]

    dNdlgx = DATA[DATA.mDM == energy][name[column_select]]
    bins_lgx = DATA[DATA.mDM == energy]['Log[10,x]']
    bins_x = 10 ** bins_lgx

    return bins_x, dNdlgx


if __name__ == '__main__':
    file_in_path = r'.\测试数据\PPPC4\AtProduction_antideuterons.dat'
    Data = pd.read_csv(file_in_path, sep='\\s+', header=0)
    bins_x, dNdlgx = read_pppc4(Data)

    plt.figure()
    plt.plot(bins_x, dNdlgx)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('dN/dlgx')
    plt.xlabel('x')
    # plt.show()

    plt.savefig(r'处理结果\图\dNdlgx_x_antideu_bb_pppc4.pdf')

    # 将数据保存为.dat文件，不保存列名与index
    DATA = pd.DataFrame({'x': bins_x, 'dNdlgx': dNdlgx})
    DATA.to_csv(r'处理结果\数据\dNdlgx_x_antideu_bb_pppc4.dat', sep='\t', index=False, header=False)

