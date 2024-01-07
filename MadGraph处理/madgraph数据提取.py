"""
Description: 提取hepmc文件中的数据，并初步处理出反质子与反中子的数据
Author: WangXiao
Param:
    1, M_DM: 暗物质质量
    2, InitDataFileDir_path: hepmc文件所在文件夹路径
    3, ChannelType: Channel类型，如bb，WW等
"""
import gc
import gzip
import os
import sys

import numpy as np


# 代码运行效率可视化
# import heartrate
# heartrate.trace(browser=True)

# 一个粒子类，用于创建数据中的粒子对象
class Particle(object):
    def __init__(self, list_of_par):
        self.barcode = int(list_of_par[1])
        self.PDGID = int(list_of_par[2])
        # self.four_momentum = list(map(float, list_of_par[3:7]))
        self.four_momentum = np.array(list_of_par[3:7]).astype(float)
        self.mass = float(list_of_par[7])
        self.status_code = int(list_of_par[8])
        self.incoming_ver_bar = int(list_of_par[9])

        self.vertex = list_of_par[-2]
        self.line_number = list_of_par[-1]

    def __repr__(self):
        return f'该粒子的PDGID为:{self.PDGID}，位于文档第{self.line_number}行'

    """ def __le__(self, other):
        if not isinstance(other, Particle):
            raise TypeError('<运算对象是Particle')
        return self.four_momentum[-1] < other.four_momentum[-1]

    def __gt__(self, other):
        if not isinstance(other, Particle):
            raise TypeError('>运算对象是Particle')
        return self.four_momentum[-1] > other.four_momentum[-1]

    def __add__(self, other):
        if not isinstance(other, Particle):
            raise TypeError('<运算对象是Particle')
        return [self.four_momentum[i]+other.four_momentum[i] for i in range(3)] """

    # 计算三动量间隔
    def computePDistance(self, other):
        if not isinstance(other, Particle):
            raise TypeError('相空间运算对象是Particle')
        pdiff = np.linalg.norm(self.four_momentum[:-1] - other.four_momentum[:-1])
        return pdiff

    # 计算四动量间隔
    def computepDistance(self, other):
        if not isinstance(other, Particle):
            raise TypeError('相空间运算对象是Particle')
        p1, p2 = self.four_momentum.copy(), other.four_momentum.copy()
        p12 = p1 - p2
        pdiff = np.sqrt(np.dot(p12[:-1], p12[:-1]) - p12[-1] ** 2)
        return pdiff

    # 计算动量大小
    def P_value(self):
        return np.linalg.norm(self.four_momentum[:-1])

    # 判断是否在同一顶点
    def issamevertex(self, other):
        if not isinstance(other, Particle):
            raise TypeError('vertex运算对象是Particle')
        vertex1, vertex2 = self.vertex, other.vertex
        # return (vertex1.event == vertex2.event) and (computeDistance(vertex1.four_x[:-1], vertex2.four_x[:-1]) < r_dbar)
        return (vertex1.event == vertex2.event) and (vertex1.four_x[:-1] == vertex2.four_x[:-1])


# 顶角类
class Vertex(object):
    def __init__(self, list_of_ver):
        self.barcode = int(list_of_ver[1])
        self.ID = int(list_of_ver[2])
        self.four_x = np.array(list_of_ver[3:7]).astype(float)
        # self.four_x = list(map(float, list_of_ver[3:7]))

        self.event = list_of_ver[-2]
        self.line_number = list_of_ver[-1]


def nplog(n_min, n_max, bins):
    return np.logspace(np.log10(n_min), np.log10(n_max), bins)


# 搜寻文件夹下所有hepmc文件
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for file in fs:
            if file.endswith('.hepmc') or file.endswith('.hepmc.gz'):
                fullname = os.path.join(root, file)
                yield fullname


PDG_pbar = -2212
PDG_nbar = -2112
# PDG_Gamma = 22  # 光子PDGID
pbar, nbar = [], []
EventsNumber = 0

# M_DM = int(input('请输入暗物质质量（单位GeV）：\n'))
# M_DM = 100
M_DM = int(sys.argv[1])  # 暗物质质量
InitDataFileDir_path = sys.argv[2]  # hepmc文件所在文件夹路径
ChannelType = sys.argv[3]  # Channel类型，如bb，WW等

# 读取数据
times = 0
for i in findAllFile(InitDataFileDir_path):
    if str(M_DM) + 'GeV' in i:
        if i.endswith('.hepmc.gz'):
            with gzip.open(i, 'rt') as f:
                lines = f.readlines()
        else:
            with open(i, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        # 从数据中挑选出开头为P的数据，即粒子，同时判断是否为反质子或反中子
        for ii in range(len(lines)):
            lines[ii] = lines[ii].split()
            if lines[ii]:
                if lines[ii][0] == 'E':
                    EventsNumber += 1  # 属于第几次模拟事件
                elif lines[ii][0] == 'V':
                    vertex_current = Vertex(lines[ii] + [EventsNumber, ii + 1])
                elif lines[ii][0] == 'P':
                    par_current = Particle(lines[ii] + [vertex_current, ii + 1])
                    # particles.append(par_current)
                    if par_current.PDGID == PDG_pbar:
                        pbar.append(par_current)
                    elif par_current.PDGID == PDG_nbar:
                        nbar.append(par_current)
                    # 如果需要其他粒子，可以在这里添加
                    # elif par_current.PDGID == PDG_Gamma:
                    #     gamma.append(par_current)
        times += 1
    if times == 5:
        break  # 先跑一部分试试

try:
    del lines  # 使用完毕，删除lines，释放内存
except NameError:
    print('未检测到对应能量的hepmc文件\n请检查!')
    exit()

# 反质子与反中子混合在一起进行统计
antinucleon = pbar + nbar

# 反质子反中子质量
mass_pbar, mass_nbar = pbar[0].mass, nbar[0].mass
M_antideuteron = 1.875612928  # 反氘核质量

bins_number = 1000  # 区间个数

Pcoal = 0.195  # 聚结动量
# r_dbar = 1e-11  # 氘核尺度半径

gc.collect()
