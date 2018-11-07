__author__ = 'David T. Pocock'


from parser import Parser
from platypus import NSGAII, Problem
from pathlib import Path
import numpy as np
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
    print(requirements)
    print(customers)
    solution = [1, 1, 1, 1]
    scored_solution = sum(get_scored_solution(solution, requirements, customers))
    print(scored_solution)


def get_scored_solution(solution, requirements, customers):
    scored_solution = []
    for i, req in enumerate(solution):
        if req:
            interested_customers = get_custs_from_req(i + 1, requirements)
            print(interested_customers)
            total_req_score = 0
            for cust in interested_customers:
                print("cust", cust)
                req_value = get_req_value_from_cust(i + 1, cust, customers)
                cust_weight = customers[cust - 1][0]
                single_req_score = req_value * cust_weight
                total_req_score += single_req_score
                print("cust value:", cust_weight, "req value:", req_value)
            scored_solution.append(total_req_score)
        else:
            scored_solution.append(0)
    return scored_solution


def get_custs_from_req(req_num, requirements):
    return requirements[req_num - 1][1]


def get_req_value_from_cust(req_num, customer, customers):
    requirements = customers[customer - 1][1]
    reversed = requirements[::-1]
    value = (reversed.index(req_num) + 1) / len(requirements)
    return value


    # rs_data = np.array(rs_fitness)
    # hs_internal = np.array(hc_internal_fitness)
    # hs_external = np.array(hc_external_fitness)
    # ga_data = np.array(ga_fitness)
    #
    # # test_cases_per_test_suite = np.array([5, 10, 20, 23, 30, 50, 100])
    # # unique_large_apfd = np.array([0.4594736842105263, 0.6063157894736844, 0.6867105263157895, 0.6978260869565216, 0.7128947368421051, 0.7326842105263159, 0.7480263157894737])
    # # full_large_apfd = np.array([0.44631578947368417, 0.6023684210526316, 0.6846052631578947, 0.6958810068649884, 0.7122807017543858, 0.7320526315789474, 0.7476578947368421])
    #
    # # plt.plot(test_cases_per_test_suite, unique_large_apfd, '-gD')
    # # plt.xlabel("Test Cases per Test Suite")
    # # plt.ylabel("Mean Fitness (APFD)")
    # # plt.xticks(np.arange(min(test_cases_per_test_suite), max(test_cases_per_test_suite) + 1, 5.0))
    #
    # ## combine these different collections into a list
    # data_to_plot = [rs_data, hs_internal, hs_external, ga_data]
    #
    # # Create a figure instance
    # fig = plt.figure(1, figsize=(9, 6))
    #
    # # Create an axes instance
    # ax = fig.add_subplot(111)
    #
    # ## add patch_artist=True option to ax.boxplot()
    # bp = ax.boxplot(data_to_plot, patch_artist=True)
    #
    # ## change outline color, fill color and linewidth of the boxes
    # for box in bp['boxes']:
    #     # change outline color
    #     box.set(color='#7570b3', linewidth=2)
    #     # change fill color
    #     box.set(facecolor='#1b9e77')
    #
    # ## change color and linewidth of the whiskers
    # for whisker in bp['whiskers']:
    #     whisker.set(color='#7570b3', linewidth=2)
    #
    # ## change color and linewidth of the caps
    # for cap in bp['caps']:
    #     cap.set(color='#7570b3', linewidth=2)
    #
    # ## change color and linewidth of the medians
    # for median in bp['medians']:
    #     median.set(color='#b2df8a', linewidth=2)
    #
    # ## change the style of fliers and their fill
    # for flier in bp['fliers']:
    #     flier.set(marker='o', color='#e7298a', alpha=0.5)
    #
    # ## Custom x-axis labels
    # ax.set_xticklabels(['Random Search', 'HC Internal Swap', 'HC External Swap', 'Genetic Algorithm'])
    #
    # ## Remove top axes and right axes ticks
    # ax.get_xaxis().tick_bottom()
    # ax.get_yaxis().tick_left()
    #
    # # Save the figure
    # graph_path = os.path.join(pwd, 'graph.pdf')
    # pdf = PdfPages(graph_path)
    # plt.savefig(pdf, format='pdf', bbox_inches='tight')
    # plt.show()
    # pdf.close()
    # pdf = None

if __name__ == "__main__":
    main()
