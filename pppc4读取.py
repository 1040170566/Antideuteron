import os

import numpy as np
from matplotlib import pyplot as plt

data = []
with open(r'/home/wangxiao/文档/AtProduction_antiprotons.dat', "r") as f:
    for line in f.readlines():
        line = line.strip("\n")
        line = line.split()
        data.append(line)

bins_lgx = np.arange(-8.9, 0.01, 0.05)
bins_lgx[-1] = 0
length_bins = len(bins_lgx)

print('首行数据为：')
name = data.pop(0)
for n in range(len(name)):
    print(f'{n}.{name[n]}')
column_select = int(input('你的选择：'))
#column_select = 13

energy_set = [int(n[0]) for n in data[0::length_bins]]
print('记录的能量为：')
for n in range(len(energy_set)):
    print(f'{n}.{energy_set[n]}')
energy_number = int(input('需要观察的能量：'))
#energy_number = 11
energy = energy_set[energy_number]
row_start = length_bins * energy_number

T = [pow(10, n) * energy for n in bins_lgx]
dndt = [float(data[n][column_select]) / np.log(10) / T[n % length_bins] for n in
        range(row_start, row_start + length_bins)]


plt.figure()
plt.plot(T, dndt)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('dN/dT (/GeV/annihilation)')
plt.xlabel('T (GeV)')
# plt.show()
plt.savefig(r'/home/wangxiao/文档/ee2bb_antip_pppc4.pdf')
#
# with open(r'/home/wangxiao/文档/dndt_t_bb.txt', 'w', encoding='utf-8') as f:
#     for w in T:
#         f.write(str(w)+'\t')
#     f.write('\n')
#     for w in dndt:
#         f.write(str(w)+'\t')

DATA = np.array([T,dndt])
np.savetxt(r'/home/wangxiao/文档/dndt_t_bb_antip_pppc4.dat', DATA)
