from population import Population
from car_customer import *
from multichromosome import Chromosome

import numpy as np
from copy import deepcopy
import random
import math
from typing import List
import matplotlib.pyplot as plt


def cal_fitness(population: Population):
    # 首先计算平均固定成本
    chromosomes = population.chromosomes
    total_cost = 0
    total_car = 0
    for i in chromosomes:
        for j in i.Chromosome:
            if len(j) == 1:
                continue
            total_car += 1
            total_cost += j[0].fixed_cost
    avg_cost = total_cost / total_car

    # 选出最优适应度和最小适应度
    max_fitness = 0
    min_fitness = 1000000
    for i in chromosomes:
        fit = i.get_fitness_value()
        if fit > max_fitness:
            max_fitness = fit
        if fit < min_fitness:
            min_fitness = fit

    # 计算正规化适应度
    fitness = []
    for i in chromosomes:
        fk = i.get_fitness_value()
        fitness.append((max_fitness + avg_cost - fk) / (max_fitness + avg_cost - min_fitness))

    return fitness


def select_the_best(p: Population):
    best = p.chromosomes[0]
    best_cost = 100000
    for i in p.chromosomes:
        x = i.get_fitness_value()
        if x < best_cost:
            best_cost = x
            best = i
    return best


# 保证每一代的最优者会留到下一代
def retain_the_best(p: Population, best: Chromosome):
    worst = p.chromosomes[0]
    worst_cost = 0
    if not p.contains(best):
        for i in p.chromosomes:
            cost = i.get_fitness_value()
            if cost > worst_cost:
                worst_cost = cost
                worst = i
        p.insert(p.index(worst), best)
        p.remove(worst)
    return p


def select(population: Population):
    fitness = cal_fitness(population)
    # 采用轮盘赌选择法
    ratio = []
    for i in fitness:
        ratio.append(i / sum(fitness))
    sum_ratio = []
    for i in range(len(ratio)):
        sum_ratio.append(sum(ratio[:i + 1]))

    next_generation = []
    for i in range(population.size):
        x = random.random()
        for j in range(population.size):
            if sum_ratio[j] > x:
                next_generation.append(population.chromosomes[j])
                break

    p = Population(population.id + 1, next_generation)

    """
    # 排序选择算法
    # 对适应度降序排序
    sorted_fitness = deepcopy(fitness)
    sorted_fitness.sort()
    sorted_fitness.reverse()

    # 将适应度前5%的个体代替掉后5%的个体
    for i in range(int(percent * len(population.chromosomes) / 100)):
        n = fitness.index(sorted_fitness[i])
        m = fitness.index(sorted_fitness[-i - 1])
    
        x = population.chromosomes[n]
        population.remove(population.chromosomes[m])
        population.insert(m, x)
    """
    return p


def euclidean_distance(source, target):
    return math.sqrt(math.pow(source.x - target.x, 2) + math.pow(source.y - target.y, 2))


'''
获得路径集 E = {d_ij | i,j ∈ V}
其中行和列索引的顺序是按照customer id从小到大，然后再从car id 从小到大
'''


def get_distance_set(car: List[Car], customer: List[Customer]):
    H = len(car)  # 车辆的总数
    N = len(customer)  # 顾客的总数
    width = N + H

    E = np.zeros((width, width))  # 路径集！(N+H)*(N+H)的一个矩阵
    # 先计算 N 个顾客相互之间的距离
    for i in range(N):
        for j in range(N):
            cus1 = customer[i]
            cus2 = customer[j]
            distance1 = euclidean_distance(cus1, cus2)
            E[cus1.id - 1][cus2.id - 1] = distance1
            E[cus2.id - 1][cus1.id - 1] = distance1

    # 再计算 H 辆车所在车场相互之间的距离
    for p in range(H):
        for q in range(H):
            car1 = car[p]
            car2 = car[q]
            distance2 = euclidean_distance(car1, car2)
            E[N + car1.id - 1][N + car2.id - 1] = distance2
            E[N + car2.id - 1][N + car1.id - 1] = distance2

    # 再计算 N个顾客和 H辆车所在车场相互之间的距离
    for m in range(N):
        for n in range(H):
            cus = customer[m]
            car1 = car[n]
            distance3 = euclidean_distance(cus, car1)
            E[cus.id - 1][N + car1.id - 1] = distance3
            E[N + car1.id - 1][cus.id - 1] = distance3

    return E


def random_color():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


def show_result(p: Population, path):
    f = open(path, "w+")

    best_path = select_the_best(p)

    path = []
    for i in range(len(best_path.car)):
        one_path = [(best_path.Chromosome[i][0].x, best_path.Chromosome[i][0].y)]
        f.write("car{} ".format(i + 1))
        for j in best_path.Chromosome[i][1:]:
            f.write(str(j.id) + ' ')
            one_path.append((j.x, j.y))
        f.write('\n')
        path.append(one_path)
    f.write("final cost is {}".format(best_path.get_fitness_value()))
    print(path)
    for one_path in path:
        color = random_color()
        for i in range(len(one_path) - 1):
            plt.plot((one_path[i][0], one_path[i + 1][0]), (one_path[i][1], one_path[i + 1][1]), color)
        plt.plot((one_path[len(one_path) - 1][0], one_path[0][0]), (one_path[len(one_path) - 1][1], one_path[0][1]),
                 color)
        plt.scatter(one_path[0][0], one_path[0][1])
    plt.savefig("result_fig")
    plt.show()
