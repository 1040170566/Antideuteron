##############################
# 建议使用madgraph数据提取.py
# 2023.08.27
##############################

import numpy as np
from matplotlib import pyplot as plt

# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']



with open(r'/home/wangxiao/MG5_aMC_v3_5_3/All_of_my_data/ee2bb/Events/run_02/100GeV_pythia8_events.hepmc', 'r',
          encoding='utf-8') as f:
    lines = f.readlines()

particles = []
PDG_pbar = -2212
PDG_nbar = -2112
pbar, nbar = [], []
EventsNumber = 0

# PDG_Gamma = 22  # 光子PDGID
# gamma = []

# 从数据中挑选出开头为P的数据，即粒子，同时判断是否为反质子或反中子
# print(len(lines))
for ii in range(len(lines)):
    lines[ii] = lines[ii].split()
    if lines[ii]:
        if lines[ii][0] == 'E':
            EventsNumber += 1  # 属于第几次模拟事件
        elif lines[ii][0] == 'V':
            vertex_current = Vertex(lines[ii] + [EventsNumber, ii + 1])
        elif lines[ii][0] == 'P':
            par_current = Particle(lines[ii] + [vertex_current, ii + 1])
            particles.append(par_current)
            if par_current.PDGID == PDG_pbar:
                pbar.append(par_current)
            elif par_current.PDGID == PDG_nbar:
                nbar.append(par_current)
            # 如果需要其他粒子，可以在这里添加
            # elif par_current.PDGID == PDG_Gamma:
            #     gamma.append(par_current)

del lines # 使用完毕，删除lines，释放内存

# 反质子与反中子混合在一起进行统计
antinucleon = pbar + nbar

# P_pbar = [p.P_value() for p in pbar]  # 反质子动量大小列表
# P_nbar = [n.P_value() for n in nbar]  # 反中子动量大小列表

# 反质子反中子质量
mass_pbar, mass_nbar = pbar[0].mass, nbar[0].mass
M_DM = particles[0].four_momentum[-1]
# M_DM = 50
M_antideuteron = 1.875612928  # 反氘核质量

bins_number = 100  # 区间个数

Pcoal = 0.195  # 聚结动量
# r_dbar = 1e-11  # 氘核尺度

# factor = 1  # 考虑正负电子交换应该有个因子2
