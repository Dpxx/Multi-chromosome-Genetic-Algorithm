from multichromosome import Chromosome
from population import Population
from car_customer import *

import random
from copy import deepcopy


# Population: self.chromosomes = chromosomes = list[Chromosome]
# Chromosome: self.Chromosome = Multichromosome = list[oneChromosome]

def two_parent_cross_over(id_A: Chromosome, id_B: Chromosome):
    gene_pool_Fab = []
    gene_pool_Fa = []
    gene_pool_Fb = []

    H = len(id_A.car)
    operation_C = random.randint(0, H - 1)  # 将要进行操作的染色体编号

    # 拷贝将要进行操作的两条染色体
    ch1 = deepcopy(id_A.Chromosome[operation_C])
    ch2 = deepcopy(id_B.Chromosome[operation_C])

    '''
    第一部分：将两条染色体a，b上相同客户基因放如基因库Fab，A染色体上独有基因放入Fa，B染色体上独有基因放入Fb
    '''
    for gene1 in ch1:
        if isinstance(gene1, Car):
            continue

        for gene2 in ch2:
            if isinstance(gene2, Car):
                continue

            # 根据id来判断是不是同一种基因
            if gene1.id == gene2.id:
                gene_pool_Fab.append(gene1)
                break

    for common_gene in gene_pool_Fab:
        if common_gene in ch1:
            ch1.remove(common_gene)
        if common_gene in ch2:
            ch2.remove(common_gene)

    for remain_gene1 in ch1:
        if isinstance(remain_gene1, Car):
            continue
        gene_pool_Fa.append(remain_gene1)

    for remain_gene2 in ch2:
        if isinstance(remain_gene2, Car):
            continue
        gene_pool_Fb.append(remain_gene2)

    '''
    第二部分：交换A，B染色体上的客户基因
    '''
    tmp_ch1 = id_A.Chromosome[operation_C][1:]
    tmp_ch2 = id_B.Chromosome[operation_C][1:]

    del id_A.Chromosome[operation_C][1:]
    del id_B.Chromosome[operation_C][1:]

    id_A.Chromosome[operation_C] += tmp_ch2
    id_B.Chromosome[operation_C] += tmp_ch1

    capacity_A = id_A.Chromosome[operation_C][0].capacity
    capacity_B = id_B.Chromosome[operation_C][0].capacity

    id_A.Chromosome[operation_C][0].capacity = capacity_B
    id_B.Chromosome[operation_C][0].capacity = capacity_A

    '''
    第三部分：A 中a以外的染色体的客户基因与Fb中的基因对比，删除染色体上相同基因
             B 中b以外的染色体的客户基因与Fa中的基因对比，删除染色体上相同基因
    '''

    for i in range(H):
        # 如果是a染色体，跳过
        if i == operation_C:
            continue

        for gene1 in id_A.Chromosome[i]:
            # 如果是车辆基因，跳过
            if isinstance(gene1, Car):
                continue

            for pool_gene1 in gene_pool_Fb:
                if gene1.id == pool_gene1.id:
                    id_A.Chromosome[i].remove(gene1)
                    id_A.Chromosome[i][0].capacity += gene1.need
                    break

    for j in range(H):
        if j == operation_C:
            continue

        for gene2 in id_B.Chromosome[j]:
            # 如果是车辆基因，跳过
            if isinstance(gene2, Car):
                continue

            for pool_gene2 in gene_pool_Fa:
                if gene2.id == pool_gene2.id:
                    id_B.Chromosome[j].remove(gene2)
                    id_B.Chromosome[j][0].capacity += gene2.need
                    break

    '''
    第四部分：将Fa 中的基因逐一插入个体A任意染色体的首基因之后的任意位置。
             之后判断车辆是否超载，直至Fa中的基因全部分配出去为止。个体B类似
    '''
    for gene_a in gene_pool_Fa:
        # 产生随机插入的染色体编号
        random_num = []
        for i in range(H):
            random_num.append(i)
        random.shuffle(random_num)

        for ch_num in random_num:
            # 随机产生要插入的染色体序号
            len_ch = len(id_A.Chromosome[ch_num])

            # 检测车辆是否超载

            if gene_a.need <= id_A.Chromosome[ch_num][0].capacity:
                # 随机产生要插入的基因位置
                gen_num = random.randint(1, len_ch)
                id_A.Chromosome[ch_num].insert(gen_num, gene_a)
                id_A.Chromosome[ch_num][0].capacity -= gene_a.need
                # gene_pool_Fa.remove(gene_a)
                break

    for gene_b in gene_pool_Fb:

        random_num = []
        for i in range(H):
            random_num.append(i)
        random.shuffle(random_num)

        for ch_num in random_num:
            # 随机产生要插入的染色体序号

            len_ch = len(id_B.Chromosome[ch_num])

            # 检测车辆是否超载
            if gene_b.need < id_B.Chromosome[ch_num][0].capacity:
                # 随机产生要插入的基因位置
                gen_num = random.randint(1, len_ch)
                id_B.Chromosome[ch_num].insert(gen_num, gene_b)
                id_B.Chromosome[ch_num][0].capacity -= gene_b.need
                # gene_pool_Fb.remove(gene_b)
                break


def cross_over(parents: Population):
    Pc = 0.5

    all_individuals = parents.chromosomes  # 所有个体的染色体组
    individual_number = len(all_individuals)  # 个体数

    for i in range(0, individual_number - 1, 2):
        multichromosome1 = all_individuals[i]
        multichromosome2 = all_individuals[i + 1]

        P = random.random()
        if P < Pc:
            two_parent_cross_over(multichromosome1, multichromosome2)

    return parents
