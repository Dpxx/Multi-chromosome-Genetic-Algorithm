from multichromosome import Chromosome
from car_customer import data_loader
from population import Population
from function import *
from mutation import mutation
from cross_over import cross_over


generation = 1000
scale = 100
customers, cars = data_loader("data_info.txt", "depot_info.txt")

matrix = get_distance_set(cars, customers)
chromosomes = []
for m in range(scale):
    chromosome = Chromosome(m, len(cars), cars, customers, matrix)
    chromosomes.append(chromosome)

p = Population(1, chromosomes)


x = []
y1 = []
for i in range(generation):
    print("Generation {}".format(i+1))
    x.append(i)

    best = deepcopy(select_the_best(p))
    p = select(p)
    p = cross_over(p)
    p = mutation(p, 0.1)
    p = retain_the_best(p, best)

    min_value = select_the_best(p).get_fitness_value()
    print(min_value)
    y1.append(min_value)
plt.plot(x, y1)
plt.savefig("Variation curve")
plt.show()

show_result(p, "result.txt")
