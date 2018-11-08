__author__ = 'David T. Pocock'

import csv


class Parser:

    def __init__(self, path):
        self.path = path

    def parse_data(self):
        with open(self.path, newline='') as file:
            num_of_levels = int(file.readline())

            concat_req_costs = []
            for level in range(0, num_of_levels):
                next(file)
                concat_req_costs.append(file.readline().split())
            flat_req_costs = [int(i) for sublist in concat_req_costs for i in sublist]
            req_costs_percent = list(map(lambda x: x / sum(flat_req_costs), flat_req_costs))
            requirements = dict(enumerate([[i,[]] for i in req_costs_percent]))

            num_of_deps = int(file.readline())
            for dep in range(0, num_of_deps):
                next(file)

            num_of_custs = int(file.readline())
            customers = []
            cust_weights = []
            for i in range(0, num_of_custs):
                customer = file.readline().split()
                del customer[1]
                cust_weights.append(int(customer.pop(0)))

                req_list = list(map(int, customer))
                customers.append(req_list)
                for num_of_req in customer:
                    requirements[int(num_of_req) - 1][1].append(i + 1)

            norm_cust_weights = list(map(lambda x: x / sum(cust_weights), cust_weights))
            norm_customers = list(zip(norm_cust_weights, customers))

        return requirements, norm_customers
