import os
import numpy as np
from matplotlib import pyplot as plt

dir_file_path = '/home/wangxiao/document/data'
file_in = 'AtProduction_antideuterons.dat'
file_in_path = os.path.join(dir_file_path, file_in)

data = []
with open(file_in_path, "r") as f:
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
#column_select = 13 # bb

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
plt.show()
fig_out = 'ee2bb_antip_pppc4.pdf'
fig_out_path = os.path.join(dir_file_path, fig_out)
plt.savefig(fig_out_path)

DATA = np.array([T,dndt])
file_out = 'dndt_t_bb_antip_pppc4.dat'
file_out_path = os.path.join(dir_file_path, file_out)
np.savetxt(file_out_path, DATA)
