"""
尝试使用pandas进行反质子数据处理，输出为dat文件。
时间：2024.3
作者：王骁
"""

import pandas as pd
# import numpy as np
# import sys
# import os
from shutil import copyfile

import argparse

############################################
# 参数获取
## 读取外部参数
parser = argparse.ArgumentParser(description='读取所需参数，')
# parser.add_argument('mass', type=int, help='暗物质质量')
# parser.add_argument('channel', type=str, help='湮灭通道')
parser.add_argument('--inpath', '-i', type=str, default='处理结果/数据', help='dat文件所在文件夹路径')
parser.add_argument('--infile','-n', type=str, help='输入数据文件名称')
parser.add_argument('--outdir', '-d', type=str, default='处理结果/数据', help='数据存储文件夹')
parser.add_argument('--outfile', '-o', type=str, default='Production_pbar.dat', help='输出文件名称')

args = parser.parse_args()
# M_DM = args.mass  # 暗物质质量
# ChannelType = args.channel  # Channel类型，如bb，WW等
InitDataFileDir = args.inpath  # dat文件所在文件夹路径
FileName = args.infile  # 数据文件名称
ResultOutputDir = args.outdir  # 数据文件存储位置
OutFileName = args.outfile # excel文件名

#############################################
DATA_path = f"{InitDataFileDir}/{FileName}"  # 读取数据文件完整路径

# 数据加载
DATA = pd.read_csv(DATA_path, header=0, delimiter='\\s+')
Label = DATA.columns.values.tolist()
bins = DATA[Label[1]].values  # 获取刻度
# dndt = DATA['dN/dlgx'].values  # 获取数据，dN/dT

############################################

############################################
# 输出区,输出至dat制作table
# 以列为单位，依次表示暗物质质量M_DM，lgx，dN/dlgx。

## 读取dat
output_path = f"{ResultOutputDir}/{OutFileName}"
DataExist = pd.read_csv(output_path, header=0, delimiter='\\s+')
copyfile(output_path, f'{output_path}.copy')
# os.system(f'copy {output_path} {output_path}.copy') # 处理前备份


## 数据合并


if len(DataExist.loc[DataExist.mDM == DATA.iloc[0, 0], Label[-1]]) == 0:
    DataMerged = pd.merge(DATA, DataExist, on=Label, how='outer')
else:
    # 将DataExist中mDM=100，'b'列的值用DATA替换
    DataExist.loc[DataExist.mDM == DATA.iloc[0, 0], Label[-1]] = DATA[Label[-1]].values
    DataMerged = DataExist
    
    

DataMerged.sort_values(by=Label[:-1], inplace=True)

DataMerged.to_csv(output_path, index=False, sep='\t')

# pd.options('display.maxcolumns', len(DataMerged))
# with open('test.dat', 'w') as f:
#     f.write(DataMerged.__repr__())
