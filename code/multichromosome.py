from car_customer import Car
from car_customer import Customer

import random
from copy import deepcopy
from typing import List
import numpy as np
import math


# Multiple chromosomes.The number of chromosomes equals to the number of car numbers
class Chromosome:
    def __init__(self, id: int, car_number: int, cars: List[Car], customers: List[Customer], matrix):

        # 打乱客户序列
        tmp_customers = deepcopy(customers)
        random.shuffle(tmp_customers)

        tmp_cars = deepcopy(cars)

        oneChromosome = []  # oneChromosome = [car,customer,customer,...] or [car]
        MultiChromosome = []  # 包含了多条染色体

        # 将每个车辆分配到每条染色体上
        for i in range(car_number):
            oneChromosome.append(tmp_cars[i])
            MultiChromosome.append(oneChromosome)
            oneChromosome = []

        # 将一个顾客分配给剩余容量足够的车辆
        for one_customer in tmp_customers:
            while True:
                j = random.randint(0, car_number - 1)
                if MultiChromosome[j][0].capacity >= one_customer.need:
                    MultiChromosome[j].append(one_customer)
                    MultiChromosome[j][0].capacity -= one_customer.need
                    break

        self.id = id
        self.car = tmp_cars
        self.customer = tmp_customers
        self.matrix = matrix
        self.Chromosome = MultiChromosome
        """
        self.need = self.save_need()
        self.capacity = self.save_capacity()
        self.Decision_varaible = self.get_decision_variable()
        self.flag = self.restrain_condition_check()
        """

    def save_need(self):
        N = len(self.customer)  # 顾客的总数
        g = np.zeros(N)
        for i in self.customer:
            g[i.id - 1] = i.need
        return g

    def save_capacity(self):
        H = len(self.car)  # 车辆的总数
        Q = np.zeros(H)
        for i in self.car:
            Q[i.id - 1] = i.capacity
        return Q

    # 计算决策变量
    def get_decision_variable(self):
        H = len(self.car)  # 车辆的总数
        N = len(self.customer)  # 顾客的总数

        x_ijh = np.zeros((H + N, H + N, H))  # 决策变量！一个三维矩阵

        for i in range(H):
            oneChromosome = self.Chromosome[i]

            # 如果一条染色体上仅有车辆自身，不进行后续操作
            if len(oneChromosome) == 1:
                continue

            start_car = oneChromosome[0]
            first_customer = oneChromosome[1]

            # 先把车场到第一个顾客的决策变量记录
            # 注意，由于数组特性，这里的第三个角标会在实际车的 id上减去 1。到时候处理需要注意
            x_ijh[N + start_car.id - 1][first_customer.id - 1][i] = 1

            # New : 再把从最后一个顾客回到车场的决策变量记录下来
            x_ijh[oneChromosome[-1].id - 1][N + start_car.id - 1][i] = 1

            # 如果一条染色体上仅有车辆及一个顾客，不进行后续操作
            if len(oneChromosome) == 2:
                continue

            # 再把顾客到顾客之间的决策变量记录
            len_oneC = len(oneChromosome)

            for j in range(1, len_oneC - 1):
                first_id = oneChromosome[j].id
                second_id = oneChromosome[j + 1].id
                x_ijh[first_id - 1][second_id - 1][i] = 1

        return x_ijh

    def get_fitness_value(self):
        total_fixed_cost = 0
        total_var_cost = 0

        H = len(self.car)  # 车辆的总数
        N = len(self.customer)  # 顾客的总数
        Decision_varaible = self.get_decision_variable()
        for h in range(H):
            oneChromosome = self.Chromosome[h]
            c_1h = oneChromosome[0].fixed_cost
            for j in range(N + H):
                for i in range(N, N + H):
                    fixed_cost = c_1h * Decision_varaible[i][j][h]
                    total_fixed_cost += fixed_cost

        for h2 in range(H):
            oneChromosome2 = self.Chromosome[h2]
            c_2h = oneChromosome2[0].var_cost
            for j2 in range(N + H):
                for i2 in range(N + H):
                    var_cost = c_2h * self.matrix[i2][j2] * Decision_varaible[i2][j2][h2]
                    total_var_cost += var_cost

        return total_fixed_cost + total_var_cost

    """                
    def restrain_condition_check(self):
        H = len(self.car)  #车辆的总数
        N = len(self.customer)

        
        item1 = 0
        flag1 = False
        for h1 in range(H):
            for j1 in range(N + H):
                for i1 in range(N,N + H):
                    item1 += self.Decision_varaible[i1][j1][h1]

        if item1 <= H:
            flag1 = True
     
        flag2 = False
        for j2 in range(N):
            item2 = 0
            for h2 in range(H):
                for i2 in range(N + H):
                    item2 += self.Decision_varaible[i2][j2][h2]
            
            if item2 == 1:
                flag2 = True
            else: 
                flag2 = False
                break
             
        flag3 = False
        for i3 in range(N):
            item3 = 0
            for h3 in range(H):
                for j3 in range(N + H):
                    item3 += self.Decision_varaible[i3][j3][h3]
            
            if item3 == 1:
                flag3 = True
            else:
                flag3 = False
                break

        flag4 = False
        for h4 in range(H):
            item4 = 0
            for j4 in range(N + H):
                for i4 in range(N):
                    item4 += self.need[i4] * self.Decision_varaible[i4][j4][h4]
            if item4 <=  self.capacity[h4]:
                flag4 = True
            else:
                flag4 = False
                break

        flag5 = False
        for h5 in range(H):
            item5_left = 0
            item5_right = 0
            for i5 in range(N + H):
                item5_left += self.Decision_varaible[i5][N + h5][h5]
            for j5 in range(N + H):
                item5_right += self.Decision_varaible[N + h5][j5][h5]
            
            if item5_left == item5_right and item5_left <=1 and item5_right <=1:
                flag5 = True
            
            else:
                flag5 = False
                break
       
        flag6 = False
        for h6 in range(H):
            item6 = 0
            for i6 in range(N,N + H):
                for j6 in range(N,N + H):
                    item6 += self.Decision_varaible[i6][j6][h6]
               
            if item6 == 0:
                flag6 = True
            else:
                flag6 = False
                break

        flag = flag1 and flag2 and flag3 and flag4 and flag5 and flag6

        return flag
    """
