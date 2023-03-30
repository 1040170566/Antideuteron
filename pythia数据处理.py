from matplotlib import pyplot as plt
import numpy as np
import csv

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


# 一个粒子类，用于创建数据中的粒子对象
class Particle(object):
    def __init__(self, list_of_par):
        self.barcode = int(list_of_par[1])
        self.PDGID = int(list_of_par[2])
        self.four_momentum = list(map(float, list_of_par[3:7]))
        self.mass = float(list_of_par[7])
        self.status_code = int(list_of_par[8])
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

    def P_value(self):
        return np.sqrt(sum(p ** 2 for p in self.four_momentum[:-1]))


def main():
    with open(r'D:\学习资料\毕业论文\模拟代码\tag_1_pythia8_events\tag_1_pythia8_events.hepmc', 'r',
              encoding='utf-8') as f:
        lines = f.readlines()

    particles = []
    PDG_pbar = -2212
    PDG_nbar = -2112
    pbar, nbar = [], []
    EventsNumber = 0

    # 从数据中挑选出开头为P的数据，即粒子，同时判断是否为反质子或反中子
    # print(len(lines))
    for ii in range(len(lines)):
        lines[ii] = lines[ii].split()
        # if lines[ii] and lines[ii][0] == 'P':
        #     particles.append(Particle(lines[ii] + [ii + 1]))
        #     if particles[-1].PDGID == PDG_pbar:
        #         pbar.append(particles[-1])
        #     else:
        #         if particles[-1].PDGID == PDG_nbar:
        #             nbar.append(particles[-1])
        # elif lines[ii] and lines[ii][0] == 'E':
        #     EventsNumber += 1

        if lines[ii]:
            if lines[ii][0] == 'P':
                particles.append(Particle(lines[ii] + [ii + 1]))
                if particles[-1].PDGID == PDG_pbar:
                    pbar.append(particles[-1])
                elif particles[-1].PDGID == PDG_nbar:
                    nbar.append(particles[-1])
            elif lines[ii][0] == 'E':
                EventsNumber += 1

    # 区间个数
    bins_number = 100

    plt.figure("1.动量分布dN/dp -p")
    # 质子动量分布
    P_pbar = [p.P_value() for p in pbar]
    Pmax_pbar, Pmin_pbar = max(P_pbar), min(P_pbar)
    # print(Pmax_pbar, Pmin_pbar)
    bins_P_pbar = np.linspace(Pmin_pbar, Pmax_pbar, bins_number + 1)
    numbers_P_pbar, bins_P_pbar = np.histogram(P_pbar, bins=bins_P_pbar)
    numbers_P_pbar = list(numbers_P_pbar)
    for x in range(len(numbers_P_pbar)):
        numbers_P_pbar[x] /= (bins_P_pbar[x + 1] - bins_P_pbar[x]) * EventsNumber
    # print(numbers_P_pbar)
    # plt.scatter(bins_P_pbar[:-1], numbers_P_pbar, s=5, label=r'$\bar{p}$')
    plt.plot(bins_P_pbar[:-1], numbers_P_pbar, label=r'$\bar{p}$')

    # 数据写入文档，用于模拟
    # f = open(r'D:\学习资料\毕业论文\模拟代码\反质子反中子动量分布.csv', 'w', encoding='utf-8')
    # f_writer = csv.writer(f)
    # f_writer.writerows([bins_P_pbar[:-1], numbers_P_pbar])

    # 中子动量分布
    P_nbar = [n.P_value() for n in nbar]
    Pmax_nbar, Pmin_nbar = max(P_nbar), min(P_nbar)
    # print(Pmax_nbar, Pmin_nbar)
    bins_P_nbar = np.linspace(Pmin_nbar, Pmax_nbar, bins_number + 1)
    numbers_P_nbar, bins_P_nbar = np.histogram(P_nbar, bins=bins_P_nbar)
    numbers_P_nbar = list(numbers_P_nbar)
    for x in range(len(numbers_P_nbar)):
        numbers_P_nbar[x] /= (bins_P_nbar[x + 1] - bins_P_nbar[x]) * EventsNumber
    # print(numbers_P_nbar)
    # plt.scatter(bins_P_nbar[:-1], numbers_P_nbar, s=5, c='r', label=r'$\bar{n}$')
    plt.plot(bins_P_nbar[:-1], numbers_P_nbar, 'r', label=r'$\bar{n}$')

    # f_writer.writerows([bins_P_nbar[:-1], numbers_P_nbar])
    # f.close()

    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('dN/dp (/GeV/annihilation)')
    plt.xlabel('p (GeV)')
    plt.legend()
    plt.title('反质子反中子动量分布')
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\反质子反中子动量分布.png')
    # plt.show()

    # 另一种动量分布图
    plt.figure("4.动量分布2 EdN/dp -p")
    mass_pbar, mass_nbar = pbar[0].mass, nbar[0].mass
    numbers2_P_pbar = numbers_P_pbar.copy()
    for x in range(len(numbers2_P_pbar)):
        numbers2_P_pbar[x] *= np.sqrt(bins_P_pbar[x] ** 2 + mass_pbar ** 2)
    # print(numbers2_P_pbar)
    # plt.scatter(bins_P_pbar[:-1], numbers2_P_pbar, s=5, label=r'$\bar{p}$')
    plt.plot(bins_P_pbar[:-1], numbers2_P_pbar, label=r'$\bar{p}$')

    numbers2_P_nbar = numbers_P_nbar.copy()
    for x in range(len(numbers2_P_nbar)):
        numbers2_P_nbar[x] *= np.sqrt(bins_P_nbar[x] ** 2 + mass_nbar ** 2)
    # print(numbers_P_nbar)
    # plt.scatter(bins_P_nbar[:-1], numbers_P_nbar, s=5, c='r', label=r'$\bar{n}$')
    plt.plot(bins_P_nbar[:-1], numbers2_P_nbar, 'r', label=r'$\bar{n}$')

    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('E dN/dp (/annihilation)')
    plt.xlabel('p (GeV)')
    plt.legend()
    plt.title('反质子反中子动量分布(2)')
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\反质子反中子动量分布(2).png')
    # plt.show()

    """
    plt.figure('5.反氘的动量分布')
    # 反质子与反中子混合在一起进行统计
    antinucleon = pbar + nbar
    P_nu = [nu.P_value() for nu in antinucleon]
    Pmax_nu, Pmin_nu = max(P_nu), min(P_nu)
    print(Pmax_nu, Pmin_nu)
    bins_P_nu = np.linspace(Pmin_nu, Pmax_nu, bins_number + 1)

    numbers_bins2_P_pbar, bins_P_nu = np.histogram(P_pbar, bins=bins_P_nu)
    numbers_bins2_P_pbar = list(numbers_bins2_P_pbar)
    for x in range(len(numbers_bins2_P_pbar)):
        numbers_bins2_P_pbar[x] /= (bins_P_nu[x + 1] - bins_P_nu[x]) * EventsNumber / np.sqrt(
            bins_P_nu[x] ** 2 + mass_pbar ** 2)
    plt.plot(bins_P_nu[:-1], numbers_bins2_P_pbar, label=r'$\bar{p}$')

    numbers_bins2_P_nbar, bins_P_nu = np.histogram(P_nbar, bins=bins_P_nu)
    numbers_bins2_P_nbar = list(numbers_bins2_P_nbar)
    for x in range(len(numbers_bins2_P_nbar)):
        numbers_bins2_P_nbar[x] /= (bins_P_nu[x + 1] - bins_P_nu[x]) * EventsNumber / np.sqrt(
            bins_P_nu[x] ** 2 + mass_nbar ** 2)
    plt.plot(bins_P_nu[:-1], numbers_bins2_P_nbar, 'r', label=r'$\bar{n}$')
    """




    # 画出总能量分布图
    plt.figure('2.能量分布EdN/dE')
    E_pbar = [p.four_momentum[-1] for p in pbar]
    Emax_pbar, Emin_pbar = max(E_pbar), min(E_pbar)
    # print(Emax_pbar, Emin_pbar)
    bins_E_pbar = np.linspace(Emin_pbar, Emax_pbar, bins_number + 1)
    numbers_E_pbar, bins_E_pbar = np.histogram(E_pbar, bins=bins_E_pbar)
    numbers_E_pbar = list(numbers_E_pbar)
    for x in range(len(numbers_E_pbar)):
        numbers_E_pbar[x] /= (bins_E_pbar[x + 1] - bins_E_pbar[x]) / bins_E_pbar[x] * EventsNumber
    # plt.scatter(bins_E_pbar[:-1], numbers_E_pbar, s=5, label=r'$\bar{p}$')
    plt.plot(bins_E_pbar[:-1], numbers_E_pbar, label=r'$\bar{p}$')

    E_nbar = [n.four_momentum[-1] for n in nbar]
    Emax_nbar, Emin_nbar = max(E_nbar), min(E_nbar)
    # print(Emax_nbar, Emin_nbar)
    bins_E_nbar = np.linspace(Emin_nbar, Emax_nbar, bins_number + 1)
    numbers_E_nbar, bins_E_nbar = np.histogram(E_nbar, bins=bins_E_nbar)
    numbers_E_nbar = list(numbers_E_nbar)
    for x in range(len(numbers_E_nbar)):
        numbers_E_nbar[x] /= (bins_E_nbar[x + 1] - bins_E_nbar[x]) / bins_E_nbar[x] * EventsNumber
    # plt.scatter(bins_E_nbar[:-1], numbers_E_nbar, s=5, c='r', label=r'$\bar{n}$')
    plt.plot(bins_E_nbar[:-1], numbers_E_nbar, 'r', label=r'$\bar{n}$')

    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('E dN/dE (/annihilation)')
    plt.xlabel('E (GeV)')
    plt.legend()
    plt.title('反质子反中子能量分布')
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\反质子反中子能量分布.png')
    # plt.show()

    """
    plt.figure('6.反氘的能量分布')
    # 反质子与反中子混合在一起进行统计
    antinucleon = pbar + nbar
    P_nu = [nu.four_momentum[-1] for nu in antinucleon]
    Emax_nu, Emin_nu = max(P_nu), min(P_nu)
    # print(Emax_nu, Emin_nu)
    bins_E_nu = np.linspace(Emin_nu, Emax_nu, bins_number + 1)

    numbers_bins2_E_pbar, bins_E_nu = np.histogram(E_pbar, bins=bins_E_nu)
    numbers_bins2_E_pbar = list(numbers_bins2_E_pbar)
    for x in range(len(numbers_bins2_E_pbar)):
        numbers_bins2_E_pbar[x] /= (bins_E_nu[x + 1] - bins_E_nu[x]) * EventsNumber
    plt.plot(bins_E_nu[:-1], numbers_bins2_E_pbar, label=r'$\bar{p}$')

    numbers_bins2_E_nbar, bins_E_nu = np.histogram(E_nbar, bins=bins_E_nu)
    numbers_bins2_E_nbar = list(numbers_bins2_E_nbar)
    for x in range(len(numbers_bins2_E_nbar)):
        numbers_bins2_E_nbar[x] /= (bins_E_nu[x + 1] - bins_E_nu[x]) * EventsNumber
    plt.plot(bins_E_nu[:-1], numbers_bins2_E_nbar, 'r', label=r'$\bar{n}$')

    Pcoal = 0.215   #聚结动量
    M_antideuteron = 1.875612928         #核质量
    # B= lambda A, Z:(4*np.pi/3*Pcoal**3)**(A-1)/np.math.factorial(A)*M_A/(mass_pbar**
    B_AP_A = 2*M_antideuteron/mass_pbar/mass_nbar*Pcoal**3/24

    numbers_bins2_E_antideuteron = []
    for x in range(bins_number):
        P_A = 
        numbers_bins2_E_antideuteron.append(B_AP_A * numbers_bins2_E_pbar[x]*numbers_bins2_E_nbar[x]/)
    """



    '''
    plt.figure(3)
    # 画出动能分布图
    T_pbar = [p.four_momentum[-1] - p.mass for p in pbar]
    Tmax_pbar, Tmin_pbar = max(T_pbar), min(T_pbar)
    # print(Tmax_pbar, Tmin_pbar)
    bins_T_pbar = np.linspace(Tmin_pbar, Tmax_pbar, bins_number + 1)
    numbers_T_pbar, bins_T_pbar = np.histogram(T_pbar, bins=bins_T_pbar)
    numbers_T_pbar = list(numbers_T_pbar)
    for x in range(len(numbers_T_pbar)):
        numbers_T_pbar[x] /= (bins_T_pbar[x + 1] - bins_T_pbar[x]) / bins_T_pbar[x] * EventsNumber
    # plt.scatter(bins_T_pbar[:-1], numbers_T_pbar, s=5, label=r'$\bar{p}$')
    plt.plot(bins_T_pbar[:-1], numbers_T_pbar, label=r'$\bar{p}$')

    T_nbar = [n.four_momentum[-1] - n.mass for n in nbar]
    Tmax_nbar, Tmin_nbar = max(T_nbar), min(T_nbar)
    # print(Emax_nbar, Emin_nbar)
    bins_T_nbar = np.linspace(Tmin_nbar, Tmax_nbar, bins_number + 1)
    numbers_T_nbar, bins_T_nbar = np.histogram(T_nbar, bins=bins_T_nbar)
    numbers_T_nbar = list(numbers_T_nbar)
    for x in range(len(numbers_T_nbar)):
        numbers_T_nbar[x] /= (bins_T_nbar[x + 1] - bins_T_nbar[x]) / bins_T_nbar[x] * EventsNumber
    # plt.scatter(bins_T_nbar[:-1], numbers_T_nbar, s=5, c='r', label=r'$\bar{n}$')
    plt.plot(bins_T_nbar[:-1], numbers_T_nbar, 'r', label=r'$\bar{n}$')

    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('T dN/dT (/annihilation)')
    plt.xlabel('T (GeV)')
    plt.legend()
    plt.title('反质子反中子动能分布')
    plt.savefig(r'D:\学习资料\毕业论文\模拟代码\反质子反中子动能分布.png')
    # plt.show()
    '''

if __name__ == '__main__':
    main()
