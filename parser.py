__author__ = 'David T. Pocock'

import csv


class Parser:

    def __init__(self, path):
        self.path = path

    def parse_data(self):
        with open(self.path, newline='') as file:
            num_of_levels = int(file.readline())

            concat_reqs = []
            for level in range(0, num_of_levels):
                next(file)
                concat_reqs.append(file.readline().split())
            requirements = dict(enumerate([[int(i),[]] for sublist in concat_reqs for i in sublist]))

            num_of_deps = int(file.readline())
            for dep in range(0, num_of_deps):
                next(file)

            num_of_custs = int(file.readline())
            customers = []
            for i in range(0, num_of_custs):
                customer = file.readline().split()
                del customer[1]
                customer_tuple = (int(customer.pop(0)), list(map(int, customer)))
                customers.append(customer_tuple)
                for num_of_req in customer:
                    requirements[int(num_of_req) - 1][1].append(i + 1)

        return requirements, customers
