__author__ = 'David T. Pocock'


from parser import Parser
from platypus import NSGAII, Problem, Binary
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os.path


def main():
    pwd = os.path.abspath(os.path.dirname(__file__))
    classic_dir_path = Path("classic-nrp/")
    realistic_dir_path = Path("realistic-nrp/")
    classic_nrp = pwd / classic_dir_path / "nrp4.txt"
    realistic_nrp = pwd / realistic_dir_path / "nrp-m1.txt"

    global requirements
    global customers
    global req_costs
    global weight

    parser = Parser(realistic_nrp)
    requirements, customers, req_costs = parser.parse_data()
    weight = 0.1

    problem = Problem(1, 2)
    problem.types[:] = Binary(len(requirements))
    # print(problem.directions)
    problem.directions[0] = Problem.MAXIMIZE
    problem.directions[1] = Problem.MINIMIZE
    problem.constraints[:] = "<=1.0"
    problem.function = multi_objective_nrp

    algorithm = NSGAII(problem)
    algorithm.run(500)

    print([solution.objectives[0] for solution in algorithm.result])
    print([solution.objectives[1] for solution in algorithm.result])

    plt.scatter([solution.objectives[0]  for solution in algorithm.result],
                 [solution.objectives[1] * (-1) for solution in algorithm.result], 15, edgecolors='black')

    problem = Problem(1, 1, 1)
    problem.types[:] = Binary(len(requirements))
    print(problem.directions)
    problem.directions[:] = Problem.MAXIMIZE
    problem.constraints[:] = "<=1.0"
    problem.function = single_objective_nrp

    algorithm = NSGAII(problem)
    algorithm.run(500)

    print([solution.objectives[0] for solution in algorithm.result])
    print([solution.constraints[0] for solution in algorithm.result])

    plt.scatter([solution.objectives[0] for solution in algorithm.result],
                [solution.constraints[0] for solution in algorithm.result], 15, color='orange', edgecolors='black')

    # plt.xlim([0, 1.1])
    # plt.ylim([0, 1.1])
    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")
    plt.show()


def single_objective_nrp(solution):
    score, cost = get_solution_vars(solution)
    fitness_function = weight * score + (1 - weight) * (cost * (-1))
    return score, cost*(-1)


def multi_objective_nrp(solution):
    score, cost = get_solution_vars(solution)
    return score, cost


def get_solution_vars(solution):
    solution = solution[0]
    total_cost = sum(req_costs)
    total_score = 0
    solution_score = 0
    solution_cost = 0
    for i, req in enumerate(solution):
        interested_customers = requirements[i]
        total_req_score = 0
        for cust in interested_customers:
            req_value = value(i + 1, cust)
            cust_weight = customers[cust - 1][0]
            single_req_score = req_value * cust_weight
            total_score += single_req_score
            total_req_score += single_req_score
        if req:
            req_cost = req_costs[i]
            solution_score += total_req_score
            solution_cost += req_cost
    return solution_score/total_score, solution_cost/total_cost


def value(req_num, customer):
    cust_reqs = customers[customer - 1][1]
    reversed_reqs = cust_reqs[::-1]
    value = (reversed_reqs.index(req_num) + 1) / len(reversed_reqs)
    return value


if __name__ == "__main__":
    main()
