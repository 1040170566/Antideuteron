"""
Description: 提取hepmc文件中的数据，并初步处理出反质子与反中子的数据
Author: WangXiao
Param:
    1, M_DM: 暗物质质量
    2, InitDataFileDir: hepmc文件所在文件夹路径
    3, ChannelType: Channel类型，如bb，WW等
"""
import argparse
import gzip
import os

from Defines import Particle, Vertex
# 代码运行效率可视化
# import heartrate
# heartrate.trace(browser=True)

#################################################################################################
# 读取外部参数
parser = argparse.ArgumentParser(description="读取所需参数，暗物质能量、路径、通道等")
parser.add_argument("mass", type=int, help="暗物质质量")
parser.add_argument("channel", type=str, help="湮灭通道")
parser.add_argument("--inputdir", "-i", type=str, default="测试数据", help="hepmc文件所在文件夹路径")
parser.add_argument("--outputdir", "-o", type=str, default="Results", help="数据存储文件夹")
parser.add_argument("--times", "-n", type=int, default=1, help="最大读取文件数")

args = parser.parse_args()
M_DM = args.mass  # 暗物质质量
ChannelType = args.channel  # Channel类型，如bb，WW等
InitDataFileDir = args.inputdir  # hepmc文件所在文件夹路径
ResultOutputDir = args.outputdir  # 数据文件存储位置
Times = args.times  # 最大读取文件数
###################################################################################################

def findAllFile(base):
    # 搜寻文件夹下所有hepmc文件
    for root, ds, fs in os.walk(base):
        for file in fs:
            if file.endswith(".hepmc") or file.endswith(".hepmc.gz"):
                fullname = os.path.join(root, file)
                yield fullname

def process_file(file_path):
    if file_path.endswith(".hepmc.gz"):
        with gzip.open(file_path, "rt") as f:
            for line in f:
                yield line
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line

def get_particles(file_path):
    # 从hepmc文件中提取粒子信息
    lines = process_file(file_path)
    EventsNumber = 0
    line_number = 0
    pbar, nbar = [], []

    # 从数据中挑选出开头为P的数据，即粒子，同时判断是否为反质子或反中子
    for line in lines:
        line_number += 1
        line = line.split()
        if line:
            if line[0] == "E":
                EventsNumber += 1  # 属于第几次模拟事件
            elif line[0] == "V":
                vertex_current = Vertex(line, EventsNumber, line_number, hepmc_file_path)
            elif line[0] == "P":
                par_current = Particle(line, vertex_current, line_number)
                # particles.append(par_current)
                if par_current.PDGID == PDG_pbar:
                    pbar.append(par_current)
                if par_current.PDGID == PDG_nbar:
                    nbar.append(par_current)
                # 如果需要其他粒子，可以在这里添加
                # if par_current.PDGID == PDG_Gamma:
                #     gamma.append(par_current)
    return pbar, nbar, EventsNumber

PDG_pbar = -2212
PDG_nbar = -2112
# PDG_Gamma = 22  # 光子PDGID

M_antideuteron = 1.875612928  # 反氘核质量，单位GeV
Pcoal = 0.195  # 聚结动量，单位GeV

EventsNumber = 0
pbar, nbar = [], []

# 读取数据
times = 0
for hepmc_file_path in findAllFile(InitDataFileDir):
    if str(M_DM) + "GeV" in hepmc_file_path:
        pbar_tmp, nbar_tmp, events = get_particles(hepmc_file_path)
        pbar += pbar_tmp
        nbar += nbar_tmp
        EventsNumber += events
        """ lines = process_file(hepmc_file_path)
        line_number = 0
        # 从数据中挑选出开头为P的数据，即粒子，同时判断是否为反质子或反中子
        for line in lines:
            line_number += 1
            line = line.split()
            if line:
                if line[0] == "E":
                    EventsNumber += 1  # 属于第几次模拟事件
                elif line[0] == "V":
                    vertex_current = Vertex(line, EventsNumber, line_number, hepmc_file_path)
                elif line[0] == "P":
                    par_current = Particle(line, vertex_current, line_number)
                    # particles.append(par_current)
                    if par_current.PDGID == PDG_pbar:
                        pbar.append(par_current)
                    if par_current.PDGID == PDG_nbar:
                        nbar.append(par_current)
                    # 如果需要其他粒子，可以在这里添加
                    # if par_current.PDGID == PDG_Gamma:
                    #     gamma.append(par_current) """
        times += 1
    if times == Times:
        break  # 先跑一部分试试
""" 
try:
    del lines  # 使用完毕，删除lines，释放内存
except NameError:
    print("未检测到对应能量的hepmc文件\n请检查!")
    exit()
 """
# 反质子与反中子混合在一起进行统计
antinucleon = pbar + nbar

# 反质子反中子质量
mass_pbar, mass_nbar = pbar[0].mass, nbar[0].mass
