from 数据提取 import *

antideuterons = []
"""for p in pbar:
    for n in nbar:
        if p.vertex.event > n.vertex.event:
            continue
        if p.vertex.event < n.vertex.event:
            break
        if p.computePDistance(n) < Pcoal:
            antideuterons.append([p, n])
"""

for p in pbar:
    event = p.vertex.event
    loc_min, loc_max = 0, len(nbar)-1

    if event < nbar[loc_min].vertex.event:
        continue
    elif event == nbar[loc_min].vertex.event:
        while event == nbar[loc_min].vertex.event:
            if p.computePDistance(nbar[loc_min]) < Pcoal:
                antideuterons.append([p, nbar[loc_min]])
            loc_min += 1
        continue
    elif event == nbar[loc_max].vertex.event:
        while event == nbar[loc_max].vertex.event:
            if p.computePDistance(nbar[loc_max]) < Pcoal:
                antideuterons.append([p, nbar[loc_max]])
            loc_max -= 1
        continue
    elif event > nbar[loc_max].vertex.event:
        break

    # 二分法查找同一事件下的反中子
    while nbar[loc_min].vertex.event < event < nbar[loc_max].vertex.event:
        loc_mid = int((loc_min + loc_max)/2)
        if loc_mid == loc_min:
            exist = False
            break
        if nbar[loc_mid].vertex.event > event:
            loc_max = loc_mid
        elif nbar[loc_mid].vertex.event <event:
            loc_min = loc_mid
        else:
            exist = True
            break

    if exist:
        k = loc_mid
        while event == nbar[k].vertex.event:
            if p.computePDistance(nbar[k]) < Pcoal:
                antideuterons.append([p, nbar[k]])
            k += 1
        k = loc_mid - 1
        while event == nbar[k].vertex.event:
            if p.computePDistance(nbar[k]) < Pcoal:
                antideuterons.append([p, nbar[k]])
            k -= 1


N_antideu = len(antideuterons)
print(N_antideu)

with open(r'D:\学习资料\毕业论文\模拟代码\反氘列表.txt', 'w', encoding='utf-8') as f:
    for anti in antideuterons:
        line = list(map(lambda x: str(x.line_number), anti))
        line.insert(1, ' ')
        line.append('\n')
        f.writelines(line)
