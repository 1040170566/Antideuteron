"""
Description: 提取hepmc文件中的数据，并初步处理出反质子与反中子的数据
Author: WangXiao
Param:
    1, M_DM: 暗物质质量
    2, InitDataFileDir: hepmc文件所在文件夹路径
    3, ChannelType: Channel类型，如bb，WW等
"""
import argparse

from Defines import File, DMAnihilationParticle
# 代码运行效率可视化
# import heartrate
# heartrate.trace(browser=True)

test=1

#################################################################################################
# 读取外部参数
parser = argparse.ArgumentParser(description="读取所需参数，暗物质能量、路径、通道等")
parser.add_argument("mass", type=int, help="暗物质质量")
parser.add_argument("channel", type=str, help="湮灭通道")
parser.add_argument("--inputdir", "-i", type=str, default="TestData/", help="hepmc文件所在文件夹路径")
parser.add_argument("--outputdir", "-o", type=str, default="Results", help="数据存储文件夹")
parser.add_argument("--times", "-n", type=int, default=1, help="最大读取文件数")

if test:
    args = parser.parse_args(['100', "bb", "-i", "../TestData/MadData/ee2bb", "-o", "../Results", "-n", "1"])
else:
    args = parser.parse_args()
M_DM = args.mass  # 暗物质质量
ChannelType = args.channel  # Channel类型，如bb，WW等
InitDataFileDir = args.inputdir  # hepmc文件所在文件夹路径
ResultOutputDir = args.outputdir  # 数据文件存储位置
Times = args.times  # 最大读取文件数
###################################################################################################

DMAnihilationParticle.set_DM_mass(M_DM)  # 暗物质质量，单位GeV

# 读取数据
target = str(M_DM) + "GeV"
# target = "100GeV_pythia8_events.hepmc"
Files = []
for current_file in File.findAllFile(InitDataFileDir, target)[:Times]:
    current_file.ReadHepMC()
    Files.append(current_file)
