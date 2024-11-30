import numpy as np
import gzip
import os

PDG_ID = {"pbar": -2212, "nbar": -2112}

def ComputeDistance(v1:list|np.ndarray, v2=0):
    # 计算两个矢量之间的距离
    return np.linalg.norm(np.array(v1)-np.array(v2))

""" 
def nplog(min, max, bins):
    return np.logspace(np.log10(min), np.log10(max), bins)
 """

# 一般粒子类
class Particle(object):
    def __init__(self, E:float, P:np.ndarray[float], mass:float=None):
        self.P = P
        self.P_value = ComputeDistance(P)
        if mass is None:
            assert E >= self.P_value, "E >= P"
            self.E = E
            self.mass = np.sqrt(E**2-self.P_value**2)
        elif E == 0:
            self.mass = mass
            self.E = np.sqrt(self.P_value**2 + mass**2)
        else:
            self.E = E
            self.mass = mass
        self.T = self.E - self.mass

    def ComputeP3Distance(self, other):
        # 计算三动量间隔
        if not isinstance(other, Particle):
            raise TypeError("相空间运算对象是Particle")
        pdiff = ComputeDistance(self.P, other.P)
        return pdiff
    
    @property
    def Ekin(self):
        if self.A == 0:
            return self.T
        return self.T/self.A

    @property
    def A(self):
        return self._A
    
    @A.setter
    def A(self, A:int):
        if not isinstance(A, int):
            raise TypeError("A is int")
        if A < 0:
            raise ValueError("A is positive")
        self._A = A

    @property
    def Z(self):
        return self._Z
    
    @Z.setter
    def Z(self, Z:int):
        self._Z = Z

# 读取hepmc文件中的粒子
class ParticleInHepMC(Particle):
    def __init__(self, line_of_particle:list[str], line_number:int):
        super().__init__(float(line_of_particle[6]), np.array(line_of_particle[3:6], dtype=float), float(line_of_particle[7]))

        # self.barcode = int(line_of_particle[1])
        self.PDGID = int(line_of_particle[2])
        # self.four_momentum = np.array(line_of_particle[3:7], dtype=float) # (px,py,pz,E), unit: GeV
        # self.mass = float(line_of_particle[7])
        self.status_code = int(line_of_particle[8]) #! 0: no meaningful; 1: final state; 2: 衰变的标准模型粒子; 4:incoming beam particle 
        # self.incoming_ver_bar = int(line_of_particle[9])

        self.line_number = line_number
        self._IsComponent = False
        
    @property
    def IsComponent(self):
        return self._IsComponent
    
    @IsComponent.setter
    def IsComponent(self, ChangedComponent:bool):
        self._IsComponent = ChangedComponent

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
        return [self.four_momentum[i]+other.four_momentum[i] for i in range(3)]
        
    def ComputeP4Distance(self, other):
        # (E1-E2)^2-(p1-p2)^2
        if not isinstance(other, ElementParticle):
            raise TypeError("相空间运算对象是Particle")
        p1, p2 = self.four_momentum.copy(), other.four_momentum.copy()
        p1[-1] = p1[-1]*1j
        p2[-1] = p2[-1]*1j
        pdiff = -ComputeDistance(p1, p2)
        return pdiff

    """

# 暗物质湮灭粒子类
class DMAnihilationParticle(Particle):
    @classmethod
    def set_DM_mass(cls, mass:float):
        cls.mass_DM = mass

    @property
    def x(self):
        return self.T/self.mass_DM
    
    @property
    def lgx(self):
        return np.log10(self.x)

class DMAnihilationCompoundParticle(DMAnihilationParticle):
    @property
    def composition(self):
        return self._composition
    
    @composition.setter
    def composition(self, comp:list[DMAnihilationParticle]):
        for i in comp:
            if not isinstance(i, DMAnihilationParticle):
                raise TypeError("组成成分应该是粒子")
        self._composition = comp

# 读取hepmc文件中的暗物质湮灭粒子
class DMAnihilationParticleInHepMC(DMAnihilationParticle, ParticleInHepMC):
    def __init__(self, line_of_particle:list[str], line_number:int):
        ParticleInHepMC.__init__(self, line_of_particle, line_number)
        DMAnihilationParticle.__init__(self, float(line_of_particle[6]), np.array(line_of_particle[3:6], dtype=float), float(line_of_particle[7]))

# 顶角类
class Vertex(object):
    def __init__(self, line_of_vertex:list[str], line_number:int):
        # self.barcode = int(line_of_vertex[1])
        # self.ID = int(line_of_vertex[2])
        # self.four_x = np.array(line_of_vertex[3:7], dtype=float) # (x,y,z,ct), unit: mm
        self.r = np.array(line_of_vertex[3:6], dtype=float)
        self.ctau = float(line_of_vertex[6])

        self.line_number = line_number
        
        self.particles = []
        self.pbar = []
        self.nbar = []

    def ComputeDistance(self, other):
        if not isinstance(other, Vertex):
            raise TypeError("运算对象是Vertex")
        return ComputeDistance(self.r, other.r)

    def add_particle(self, particle:ParticleInHepMC):
        self.particles.append(particle)

    def add_pbar(self, particle:ParticleInHepMC):
        self.pbar.append(particle)

    def add_nbar(self, particle:ParticleInHepMC):
        self.nbar.append(particle)

# 事件类
class Event(object):
    def __init__(self, line_of_event:list[str], line_number:int):
        self.generated_vertices_number = int(line_of_event[8])
        self.event_id = line_number

        self.vertices = []

    @property
    def vertices_number(self):
        return len(self.vertices)

    def add_vertex(self, vertex:Vertex):
        self.vertices.append(vertex)

    def get_pbar(self):
        pbar = []
        for vertex in self.vertices:
            pbar += vertex.pbar
        return pbar
    
    def get_nbar(self):
        nbar = []
        for vertex in self.vertices:
            nbar += vertex.nbar
        return nbar

# 文件类
class File(object):
    def __init__(self, path:str):
        self.path = path

        self.events = []

    @property
    def events_number(self):
        return len(self.events)

    @property
    def get_line(self):
        if self.path.endswith(".hepmc.gz"):
            with gzip.open(self.path, "rt") as f:
                for line in f:
                    yield line
        else:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    yield line

    def ReadHepMC(self):
        line_number = 0
        for line in self.get_line:
            line_number += 1
            line = line.split()
            if line:
                if line[0] == "E":
                    current_event = Event(line, line_number)
                    self.add_event(current_event)
                elif line[0] == "V":
                    current_vertex = Vertex(line, line_number)
                    flag = 0 # 只保存存在反质子或反中子的顶点
                elif line[0] == "P":
                    current_particle = DMAnihilationParticleInHepMC(line, line_number)
                    if current_particle.PDGID == PDG_ID["pbar"]:
                        current_particle.A = 1
                        current_particle.Z = -1
                        current_vertex.add_pbar(current_particle)
                        flag += 1
                    elif current_particle.PDGID == PDG_ID["nbar"]:
                        current_particle.A = 1
                        current_particle.Z = 0
                        current_vertex.add_nbar(current_particle)
                        flag += 1
                    else:
                        continue
                    if flag == 1:
                        current_event.add_vertex(current_vertex)
                    # 如果需要其他粒子，可以在这里添加
                    # if par_current.PDGID == PDG_Gamma:
                    #     gamma.append(par_current)
        
    @classmethod
    def findAllFile(cls, base:str, target:str):
        # 搜寻文件夹下所有hepmc文件
        if not os.path.exists(base):
            raise FileNotFoundError("文件夹不存在")
        cls.BaseDir = base
        cls.Target = target
        result = []
        for root, ds, fs in os.walk(base):
            for file in fs:
                if (file.endswith(".hepmc") or file.endswith(".hepmc.gz")) and (target in file):
                    fullname = os.path.join(root, file)
                    result.append(cls(fullname))
        return result

    def add_event(self, event:Event):
        self.events.append(event)

    def get_pbar(self):
        pbar = []
        for event in self.events:
            pbar += event.get_pbar()
        return pbar
    
    def get_nbar(self):
        nbar = []
        for event in self.events:
            nbar += event.get_nbar()
        return nbar

    def get_antinucleons(self):
        return self.get_pbar() + self.get_nbar()
    
    def reset_component(self):
        for i in self.get_antinucleons():
            i.IsComponent = False
    
if __name__ == "__main__":
    a = File("../TestData/tag_1_pythia8_events.hepmc")
    a.ReadHepMC()