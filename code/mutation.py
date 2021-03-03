from multichromosome import Chromosome
from population import Population
from car_customer import Car
from car_customer import Customer

import random
from copy import deepcopy
from typing import List


def mutation(population: Population, p):
    car_number = len(population.chromosomes[0].Chromosome)
    # 对于每个个体
    for i in population.chromosomes:

        # 对每个客户基因判断是否突变，创建突变客户集
        mutation_customers = []
        for customer in i.customer:
            r = random.random()
            if r < p:
                mutation_customers.append(customer)

        # 在染色体上删去这些客户基因
        for mutation_customer in mutation_customers:
            for oneChromosome in i.Chromosome:
                if mutation_customer in oneChromosome:
                    oneChromosome.remove(mutation_customer)
                    oneChromosome[0].capacity += mutation_customer.need

        # 将突变基因再随机插回任意染色体的首基因后的任意位置
        for mutation_customer in mutation_customers:

            random_num = []
            for carnumber in range(car_number):
                random_num.append(carnumber)
                random.shuffle(random_num)

            for ch_num in random_num:
                # 随机产生要插入的染色体序号
                len_ch = len(i.Chromosome[ch_num])

                # 检测车辆是否超载

                if mutation_customer.need <= i.Chromosome[ch_num][0].capacity:
                    # 随机产生要插入的基因位置
                    gen_num = random.randint(1, len_ch)
                    i.Chromosome[ch_num].insert(gen_num, mutation_customer)
                    i.Chromosome[ch_num][0].capacity -= mutation_customer.need
                    break
            """
            while True:
                number = random.randint(0,car_number-1)
                if i.Chromosome[number][0].capacity >= mutation_customer.need:
                    length = len(i.Chromosome[number])
                    index = random.randint(1,length)
                    i.Chromosome[number].insert(index,mutation_customer)
                    i.Chromosome[number][0].capacity -= mutation_customer.need
                    break
            """

    return population
