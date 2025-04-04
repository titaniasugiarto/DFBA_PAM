import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import seaborn as sns
import pandas as pd


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

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx() #create a second plot for high value metabolites

    # Use different colormaps for 'normal' and 'high concentration' metabolites
    normal_colors = sns.color_palette('Set1')
    high_value_colors = sns.color_palette('Set2')
    normal_idx, high_value_idx = 0,0

    # for plotting experimental batch data
    exp_data = pd.read_excel('Data/Batch_fermentation_data.xlsx', 'Tabelle1')

    for metabolite, index in pos_ex_met.items():
        if only_positive and not np.any(y[:, index] > 0.1):
            continue
        if metabolite == "BIOMASS_Ecoli_core_w_GAM": # plot the data on different y-axis with different scaling because of their high value
            ax2.plot(t, y[:, index], label=metabolite, color= high_value_colors[high_value_idx])
            ax2.scatter(exp_data['t [1/h]'], exp_data[metabolite], color= high_value_colors[high_value_idx])
            high_value_idx += 1

        elif np.any((y[:, index] < -0.1) | (y[:, index] > 0.1)):
            ax1.plot(t, y[:, index], label=metabolite, color=normal_colors[normal_idx])
            ax1.scatter(exp_data['t [1/h]'], exp_data[metabolite], color=normal_colors[normal_idx])
            normal_idx += 1

    ax2.set_ylabel('Concentration')
    ax2.legend(loc='upper right', bbox_to_anchor=(1.12, 1))
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Concentration')
    ax1.legend(loc='upper left', bbox_to_anchor=(-0.17, 1))

    plt.title('Dynamic FBA: Metabolite Concentrations over Time')

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
