from 数据提取 import *

antideuteron = []
for p in pbar:
    nbar_filter = list(filter(p.issamevertex, nbar))
    for n in nbar_filter:
        if p.computePDistance(n) < Pcoal:
            antideuteron.append([p, n])

print(antideuteron)
