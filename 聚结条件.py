from 数据提取 import *

def checknearcoal(local, direction='after'):
    while event == nbar[local].vertex.event:
        if p.computepDistance(nbar[local]) < Pcoal and p.issamevertex(nbar[local]):
        # if p.computepDistance(nbar[local]) < Pcoal:
            antideuterons.append([p, nbar[local]])
        if direction == 'after':
            local += 1
        elif direction == 'before':
            local -= 1
        else:
            raise ValueError('local只能是after或者before')

antideuterons = []
for p in pbar:
    event = p.vertex.event
    loc_min, loc_max = 0, len(nbar) - 1

    if event < nbar[loc_min].vertex.event:
        continue
    elif event == nbar[loc_min].vertex.event:
        checknearcoal(loc_min)
        continue
    elif event == nbar[loc_max].vertex.event:
        checknearcoal(loc_max, 'before')
        continue
    elif event > nbar[loc_max].vertex.event:
        break

    # 二分法查找同一事件下的反中子
    while nbar[loc_min].vertex.event < event < nbar[loc_max].vertex.event:
        loc_mid = int((loc_min + loc_max) / 2)
        if loc_mid == loc_min:
            exist = False
            break
        if nbar[loc_mid].vertex.event > event:
            loc_max = loc_mid
        elif nbar[loc_mid].vertex.event < event:
            loc_min = loc_mid
        else:
            exist = True
            break

    if exist:
        checknearcoal(loc_mid)
        checknearcoal(loc_mid-1, 'before')

N_antideu = len(antideuterons)
print(N_antideu/EventsNumber)

with open(r'D:\学习资料\毕业论文\模拟代码\反氘列表.txt', 'w', encoding='utf-8') as f:
    for anti in antideuterons:
        line = list(map(lambda x: str(x.line_number), anti))
        line.insert(1, ' ')
        line.append('\n')
        f.writelines(line)
