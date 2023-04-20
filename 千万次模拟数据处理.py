import numpy as np

# 计算两个矢量之间的距离
def computeDistance(v1, v2):
    if len(v1) != len(v2):
        raise TypeError('两个矢量必须相同长度')
    l = len(v1)
    diff = []
    for x in range(l):
        diff.append(v1[x] - v2[x])
    return np.sqrt(sum(d ** 2 for d in diff))

def nplog(min, max, bins):
    return np.logspace(np.log10(min), np.log10(max), bins)

# 一个粒子类，用于创建数据中的粒子对象
class Particle(object):
    def __init__(self, list_of_par):
        self.barcode = int(list_of_par[1])
        self.PDGID = int(list_of_par[2])
        self.four_momentum = list(map(float, list_of_par[3:7]))
        self.mass = float(list_of_par[7])
        self.status_code = int(list_of_par[8])
        self.incoming_ver_bar = int(list_of_par[9])

        self.vertex = list_of_par[-2]
        self.line_number = list_of_par[-1]

    def __repr__(self):
        return f'该粒子的PDGID为:{self.PDGID}，位于文档第{self.line_number}行'

    def __le__(self, other):
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
        return [self.four_momentum[i]+other.four_momentum[i] for i in range(3)]


    # 计算三动量间隔
    def computePDistance(self, other):
        if not isinstance(other, Particle):
            raise TypeError('相空间运算对象是Particle')
        pdiff = computeDistance(self.four_momentum[:-1], other.four_momentum[:-1])
        return pdiff

    # 计算四动量间隔
    def computepDistance(self, other):
        if not isinstance(other, Particle):
            raise TypeError('相空间运算对象是Particle')
        p1, p2 = self.four_momentum.copy(), other.four_momentum.copy()
        p1[-1] = p1[-1]*1j
        p2[-1] = p2[-1]*1j
        pdiff = computeDistance(p1, p2)
        return pdiff

    def P_value(self):
        return np.sqrt(sum(p ** 2 for p in self.four_momentum[:-1]))

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
        self.four_x = list(map(float, list_of_ver[3:7]))

        self.event = list_of_ver[-2]
        self.line_number = list_of_ver[-1]


def checkcoal(p, n):
    return p.computepDistance(n) < Pcoal and p.issamevertex(n)
    # return p.computepDistance(nbar[local]) < Pcoal


with open(r"D:\个人文件\下载\ee2WW.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for ii in range(len(lines)):
    lines[ii] = lines[ii].split()

EventsNumber=0
PDG_pbar = -2212
PDG_nbar = -2112
Pcoal = 0.195
antideuterons = []

ii=0
while ii < len(lines):
    # if lines[ii][0] == 'E':
    EventsNumber += 1  # 属于第几次模拟事件
    ii +=1
    pbar, nbar = [], []
    while (ii < len(lines) and lines[ii][0] != 'E'):
        if lines[ii][0] == 'V':
            vertex_current = Vertex(lines[ii] + [EventsNumber, ii + 1])
        elif lines[ii][0] == 'P':
            par_current = Particle(lines[ii] + [vertex_current, ii + 1])
            if par_current.PDGID == PDG_pbar:
                pbar.append(par_current)
            elif par_current.PDGID == PDG_nbar:
                nbar.append(par_current)
        ii +=1

    if pbar and nbar :
        for p in pbar:
            for n in nbar:
                if checkcoal(p, n):
                    antideuterons.append([p, n])

