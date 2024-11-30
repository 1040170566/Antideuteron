# 提取pppc4的数据
import pandas as pd
from matplotlib import pyplot as plt


def read_pppc4(file_path:str, mDM:int, channel:str):
    DATA = pd.read_csv(file_path, sep='\\s+', header=0)

    dNdlgx = DATA[DATA.mDM == mDM][channel]
    bins_lgx = DATA[DATA.mDM == mDM]['Log[10,x]']
    bins_x = 10 ** bins_lgx

    return bins_x, dNdlgx, bins_lgx

def read_cosmiXs(file_path:str, mDM:int, channel:str):
    DATA = pd.read_csv(file_path, sep='\\s+', skiprows=1, header=None, names=["mDM", "Log10(x)", "uu", "dd", "cc", "bb", "tt", "gg", "WW", "ZZ", "HH"])
    # print(f"==>> DATA: {DATA}")

    dNdlgx = DATA[DATA.mDM == mDM][channel]
    bins_lgx = DATA[DATA.mDM == mDM]["Log10(x)"]
    bins_x = 10 ** bins_lgx

    return bins_x, dNdlgx

if __name__ == '__main__':
    # PPPC4FilePath = "./TestData/PPPC4/AtProduction_antiprotons.dat"
    # bins_x, dNdlgx = read_pppc4(PPPC4FilePath, 100, 'b')
    CosmiXsFilePath = "./TestData/AntiDeuterons/AtProduction-AntiD-GWF.dat"
    bins_x, dNdlgx = read_cosmiXs(CosmiXsFilePath, 100, 'bb')
    # print(f"==>> bins_x: {bins_x}")
    # print(f"==>> dNdlgx: {dNdlgx}")

    plt.figure()
    plt.plot(bins_x, dNdlgx)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('dN/dlgx')
    plt.xlabel('x')
    # plt.ylim(1e-2, 1e1)
    plt.show()

    # plt.savefig(r'Results/Figures/dNdlgx_x_antideu_bb_pppc4.pdf')

    # 将数据保存为.dat文件，不保存列名与index
    # DATA = pd.DataFrame({'x': bins_x, 'dNdlgx': dNdlgx})
    # DATA.to_csv(r'Results/Data/dNdlgx_x_antideu_bb_pppc4.dat', sep='\t', index=False, header=False)

