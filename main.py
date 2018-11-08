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

    parser = Parser(realistic_nrp)
    requirements, customers = parser.parse_data()

    problem = Problem(1, 2)
    problem.types[:] = Binary(len(requirements))
    problem.directions[0] = Problem.MAXIMIZE
    problem.directions[1] = Problem.MINIMIZE
    problem.function = multi_objective_nrp

    algorithm = NSGAII(problem)
    algorithm.run(10000)

    plt.scatter([solution.objectives[1] for solution in algorithm.result],
                 [solution.objectives[0] for solution in algorithm.result], edgecolors='black')
    plt.xlim([0, 1.1])
    plt.ylim([0, 1.1])
    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")
    plt.show()


def single_objective_nrp(solution, weight, requirements, customers):
    score, cost = get_solution_vars(solution, requirements, customers)
    fitness_function = weight * score + (1 - weight) * (cost * (-1))
    return fitness_function


def multi_objective_nrp(solution, requirements, customers):
    score, cost = get_solution_vars(solution, requirements, customers)
    return score, cost


def get_solution_vars(solution, requirements, customers):
    scored_solution = []
    solution_cost = []
    for i, req in enumerate(solution):
        if req:
            interested_customers = requirements[i][1]
            total_req_score = 0
            cost = requirements[i][0]
            for cust in interested_customers:
                req_value = get_req_value_from_cust(i + 1, cust, customers)
                cust_weight = customers[cust - 1][0]
                single_req_score = req_value * cust_weight
                total_req_score += single_req_score
            scored_solution.append(total_req_score)
            solution_cost.append(cost)
        else:
            scored_solution.append(0)
            solution_cost.append(0)
    return sum(scored_solution), sum(solution_cost)


def get_solution_cost(solution, requirements):
    solution_cost = []
    for i, req in enumerate(solution):
        if req:
            cost = requirements[i][0]
            solution_cost.append(cost)
        else:
            solution_cost.append(0)
    return sum(solution_cost)


def get_req_value_from_cust(req_num, customer, customers):
    requirements = customers[customer - 1][1]
    reversed_reqs = requirements[::-1]
    value = (reversed_reqs.index(req_num) + 1) / len(requirements)
    return value


if __name__ == "__main__":
    main()
