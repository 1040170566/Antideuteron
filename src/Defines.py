import numpy as np


def ComputeDistance(v1, v2=0):
    # 计算两个矢量之间的距离
    return np.linalg.norm(np.array(v1)-np.array(v2))


def nplog(min, max, bins):
    return np.logspace(np.log10(min), np.log10(max), bins)


class Particle(object):
    # 一个粒子类，用于存储数据中的粒子对象
    def __init__(self, list_of_par:list[str], vertex, line_number):
        self.barcode = int(list_of_par[1])
        self.PDGID = int(list_of_par[2])
        self.four_momentum = np.array(list_of_par[3:7], dtype=float) # (px,py,pz,E)
        self.mass = float(list_of_par[7])
        self.status_code = int(list_of_par[8])
        self.incoming_ver_bar = int(list_of_par[9])

        self.vertex = vertex
        self.line_number = line_number

    def __repr__(self):
        return f'该粒子的PDGID为:{self.PDGID}，位于文档\"{self.vertex.file_path}\"第{self.line_number}行'

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


    def ComputeP3Distance(self, other):
        # 计算三动量间隔
        if not isinstance(other, Particle):
            raise TypeError("相空间运算对象是Particle")
        pdiff = ComputeDistance(self.four_momentum[:-1], other.four_momentum[:-1])
        return pdiff
    
    def ComputeP4Distance(self, other):
        # (E1-E2)^2-(p1-p2)^2
        if not isinstance(other, Particle):
            raise TypeError("相空间运算对象是Particle")
        p1, p2 = self.four_momentum.copy(), other.four_momentum.copy()
        p1[-1] = p1[-1]*1j
        p2[-1] = p2[-1]*1j
        pdiff = -ComputeDistance(p1, p2)
        return pdiff

    def get_value_p3(self):
        return ComputeDistance(self.four_momentum[:-1])

    def IsSameVertex(self, other):
        if not isinstance(other, Particle):
            raise TypeError("vertex运算对象是Particle")
        vertex1, vertex2 = self.vertex, other.vertex
        r_dbar = 3 #TODO: fm
        return (vertex1.event == vertex2.event) and (ComputeDistance(vertex1.four_x[:-1], vertex2.four_x[:-1]) <= r_dbar)
        # return (vertex1.event == vertex2.event) and (vertex1.four_x[:-1] == vertex2.four_x[:-1])


# 顶角类
class Vertex(object):
    def __init__(self, list_of_ver, event, line_number, file_path):
        self.barcode = int(list_of_ver[1])
        self.ID = int(list_of_ver[2])
        self.four_x = np.array(list_of_ver[3:7], dtype=float) # (x,y,z,t)

        self.event = event
        self.line_number = line_number
        self.file_path = file_path
