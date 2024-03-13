from matplotlib import pyplot as plt
import numpy as np

# 读取pppc4
data1 = np.loadtxt(r'处理结果\数据\dNdlgx_x_antideu_bb_pppc4.dat').T
# with open(r'处理结果\数据\dNdlgx_x_antideu_bb_pppc4.dat', "r") as f:
#     for line in f.readlines():
#         line = line.strip("\n")
#         line = line.split()
#         data1.append(list(map(lambda x: float(x), line)))

# 读取MG
data2 = np.loadtxt(r'处理结果\数据\dNdlgx_x_antideu_bb_MG.dat').T
# with open(r'处理结果\数据\dNdlgx_x_antideu_bb_MG.dat', "r") as f:
#     for line in f.readlines():
#         line = line.strip("\n")
#         line = line.split()
#         data2.append(list(map(lambda x: float(x), line)))


plt.figure()
plt.plot(data1[0], data1[1], 'r', label='pppc4')
plt.plot(data2[0], data2[1], 'b', label='MG')
# plt.xlim(1e-4, 1e2)
plt.ylim(1e-7, 1e-3)
plt.xscale('log')
plt.yscale('log')
# plt.ylabel('dN/dT (/GeV/annihilation)')
# plt.xlabel('T (GeV)')
plt.legend()
# plt.savefig('/home/wangxiao/文档/compare_antip_p_M.pdf')
plt.show()