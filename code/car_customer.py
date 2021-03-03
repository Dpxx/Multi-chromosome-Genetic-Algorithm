import os


class Customer:
    def __init__(self, id, x, y, need):
        self.id = id
        self.x = x
        self.y = y
        self.need = need


class Car:
    def __init__(self, id, type, depot_id, pos, cost, capacity):
        self.id = id
        self.depot_id = depot_id
        self.type = type

        self.x = pos[0]
        self.y = pos[1]

        self.fixed_cost = cost[0]
        self.var_cost = cost[1]

        self.capacity = capacity


def data_loader(data_path, depot_path):
    if not os.path.exists(data_path):
        raise Exception('{} does not exists.'.format(data_path))
    if not os.path.exists(depot_path):
        raise Exception('{} does not exists.'.format(depot_path))

    with open(data_path, encoding='utf-8') as f:
        lines1 = f.read().split('\n')
    customer_count = int(lines1[0].split(' ')[0])
    car_count = int(lines1[0].split(' ')[1])

    with open(depot_path, encoding='utf-8') as g:
        lines2 = g.read().split('\n')
    depot_count = int(lines2[0].split(' ')[0])
    car_type_count = int(lines2[0].split(' ')[1])
    depot_pos = {}
    car_cost = {}
    car_capacity = {}
    for line in lines2[1:depot_count+1]:
        attrs = line.split(' ')
        depot_pos[int(attrs[0])] = (float(attrs[1]), float(attrs[2]))
    for line in lines2[depot_count+1:depot_count+car_type_count+1]:
        attrs = line.split(' ')
        car_capacity[int(attrs[0])] = float(attrs[1])
        car_cost[int(attrs[0])] = (float(attrs[2]), float(attrs[3]))

    customers = []
    for line in lines1[1:customer_count+1]:
        attrs = line.split(' ')
        customer = Customer(int(attrs[0]), float(attrs[1]), float(attrs[2]), float(attrs[3]))
        customers.append(customer)

    cars = []
    for line in lines1[customer_count+1:customer_count+car_count+1]:
        attrs = line.split(' ')
        car = Car(int(attrs[0]), int(attrs[1]), int(attrs[2]), depot_pos[int(attrs[2])], car_cost[int(attrs[1])], car_capacity[int(attrs[1])])
        cars.append(car)
    return customers, cars

