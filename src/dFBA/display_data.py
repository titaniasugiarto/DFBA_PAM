import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


def data_list_output(t, y, pos_ex_met):
    headers = ["Time"] + list(pos_ex_met.keys())  # Add "Time" as the first header
    non_zero_indices = list(range(len(pos_ex_met)))  # Include all indices

    data = []
    for i in range(len(t)):
        data_line = [f'{t[i]:.2f}'] + [f'{y[i, j]:.2f}' for j in non_zero_indices]
        data.append(data_line)

    print(tabulate(data, headers=headers, tablefmt='grid'))

# def data_list_output(t, y, pos_ex_met):
#     expected_length = len(pos_ex_met)
#     if y.shape[1] != expected_length:
#         raise ValueError(f"Mismatch in expected columns: {expected_length} vs {y.shape[1]}")

#     non_zero_indices = []
#     for j in range(y.shape[1]):
#         if np.any(y[:, j] != 0):
#             non_zero_indices.append(j)

#     if not non_zero_indices:
#         print("Alle Datenreihen sind die ganze Zeit 0.")
#         return

#     header = ["Time"] + [list(pos_ex_met.keys())[j] for j in non_zero_indices]
#     print("\t".join(header))

#     for i in range(len(t)):
#         data_line = [f'{t[i]:.2f}'] + [f'{y[i, j]:.2f}' for j in non_zero_indices]
#         print("\t".join(data_line))


def plot_data(t, y, pos_ex_met, plot_ids=None, exclude_ids=None, only_positive=False, plot_biomass_separately=False):
    num_metabolites = len(pos_ex_met)

    if plot_ids:
        pos_ex_met = {k: v for k, v in pos_ex_met.items() if k in plot_ids}
    if exclude_ids:
        pos_ex_met = {k: v for k, v in pos_ex_met.items() if k not in exclude_ids}

    biomass_id = None
    if plot_biomass_separately:
        biomass_id = list(pos_ex_met.keys())[-1]  # Assuming the last one is the biomass

    for metabolite, index in pos_ex_met.items():
        if only_positive and not np.any(y[:, index] > 0.1):
            continue
        if np.any((y[:, index] < -0.1) | (y[:, index] > 0.1)):
            plt.plot(t, y[:, index], label=metabolite)

    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Dynamic FBA: Metabolite Concentrations over Time')

    if plt.gca().get_legend_handles_labels()[1]:
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    else:
        print("Keine Labels für die Legende gefunden.")

    plt.grid()
    plt.show()

    if plot_biomass_separately and biomass_id:
        biomass_index = pos_ex_met[biomass_id]
        plt.plot(t, y[:, biomass_index], label=biomass_id)
        plt.xlabel('Time')
        plt.ylabel('Biomass Concentration')
        plt.title('Dynamic FBA: Biomass Concentration over Time')
        plt.grid()
        plt.legend()
        plt.show()
