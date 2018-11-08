__author__ = 'David T. Pocock'


import random
from parser import Parser
from platypus import NSGAII, Problem, Binary, GeneticAlgorithm
from pathlib import Path
import seaborn as sns; sns.set()
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
    global budget
    global runs

    parser = Parser(realistic_nrp)
    requirements, customers, req_costs = parser.parse_data()
    weight = 0.9
    budget = 0.7
    runs = 10000

    mo_problem = Problem(2, 2, 2)
    mo_problem.types[:] = Binary(len(requirements))
    mo_problem.directions[0] = Problem.MAXIMIZE
    mo_problem.directions[1] = Problem.MINIMIZE
    mo_problem.constraints[:] = "<={}".format(budget)
    mo_problem.function = multi_objective_nrp
    mo_nsga = NSGAII(mo_problem)
    mo_nsga.run(runs)

    so_problem = Problem(1, 1, 1)
    so_problem.types[:] = Binary(len(requirements))
    so_problem.directions[:] = Problem.MAXIMIZE
    so_problem.constraints[:] = "<={}".format(budget)
    so_problem.function = single_objective_nrp
    so_algorithm = GeneticAlgorithm(so_problem)
    so_algorithm.run(runs)

    random_vars = run_random(runs)

    fig = plt.figure(figsize=(10, 6))
    plt.scatter([solution.objectives[0] for solution in mo_nsga.result],
                [solution.objectives[1] * (-1) for solution in mo_nsga.result], 15, edgecolors='black')
    plt.scatter([solution.objectives[0] for solution in so_algorithm.result],
                [solution.constraints[0] * (-1) for solution in so_algorithm.result], 15, color='red', edgecolors='black')
    plt.scatter([var[0] for var in random_vars],
                [var[1] * (-1) for var in random_vars], 5, marker='+')

    plt.title("Algorithm Performance Comparison - 10000 runs")
    plt.xlabel("Score")
    # plt.xlim([0, 1.1])
    plt.ylabel("-1*Cost")
    # plt.ylim([0, 1.1])
    plt.legend(('NSGA−II', 'Single-Objective GA', 'Random search'))
    fig.savefig('algo_compared.pdf', bbox_inches="tight")


def single_objective_nrp(solution):
    score, cost = get_solution_vars(solution)
    fitness_function = weight * score + (1 - weight) * (cost)
    return fitness_function, cost


def multi_objective_nrp(solution):
    score, cost = get_solution_vars(solution)
    return [score, cost], [cost, cost]


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


def run_random(runs):
    random_vars = []
    for run in range(runs):
        score, cost = get_solution_vars(generate_random_solution())
        random_vars.append((score, cost))
    return random_vars


def generate_random_solution():
    solution = [[random.randint(0, 1) for i in range(len(requirements))]]
    return solution


if __name__ == "__main__":
    main()
