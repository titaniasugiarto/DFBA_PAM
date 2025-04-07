from cobra.io import read_sbml_model
import numpy as np
import pickle
import os
import pandas as pd
from datetime import datetime

# Defining the type aliases
TimeArray = np.ndarray
ConcentrationArray = np.ndarray

def load_model(path: str):  # Unterschiedliche reader einfügen

    extension = os.path.splitext(path)[1].lower()

    if extension == '.pkl':
    
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model
    
    elif extension in ['.xml', '.sbml']:
        model = read_sbml_model(path)
        return model
    
    else:
        raise ValueError(f"Unsupported file extension: {extension}. Supported extensions are .pkl, .xml, .sbml.")
    


def set_objective(model, objective_function_id: str):
    model.objective = objective_function_id


def position_exchange_reactions(model, objective_function_id: str):
    pos_ex_reac = {}
    position = 0
    for exchange_reaction in model.exchanges:
        exchange_metabolite_id = exchange_reaction.id
        pos_ex_reac[exchange_metabolite_id] = position
        position += 1

    # Füge die Biomasse hinzu
    pos_ex_reac[objective_function_id] = position

    return pos_ex_reac


def set_start_concentrations(start_concentrations, pos_ex_reac):
    # list_start_concentration = [0.0] * len(pos_ex_reac)
    y0 = np.zeros(len(pos_ex_reac))

    for reac_id, concentration in start_concentrations.items():
        if reac_id in pos_ex_reac:
            y0[pos_ex_reac[reac_id]] = concentration
        else:
            print(f"Warning: Metabolite {reac_id} not found in position mapping.")

    return y0


def rhs(rhs_definition):
    if rhs_definition == 1:
        print('hi')

def create_parameter_table(start_concentrations:dict, michaelis_menten_parameters:dict)-> pd.DataFrame:
    '''
    Create a parameter table containing the initial metabolite concentrations, KM, and Vmax values


    Args:
        start_concentrations: {'metabolite_1': init_conc1,
                               'metabolite_2': init_conc2}
        michaelis_menten_parameters: {'metabolite_1': {KM1: , Vmax1: },
                                      'metabolite_2': {KM1: , Vmax1: }}

    Return:
        pandas Dataframe with the parameters

    '''
    # Convert start_concentrations to a DataFrame
    parameter_table = pd.DataFrame.from_dict(start_concentrations, orient='index', columns=['Concentration'])
    parameter_table.reset_index(inplace=True)
    parameter_table.rename(columns={'index': 'Metabolite'}, inplace=True)

    # Convert michaelis_menten_parameters to a DataFrame
    mm_df = pd.DataFrame.from_dict(michaelis_menten_parameters, orient='index')
    mm_df.reset_index(inplace=True)
    mm_df.rename(columns={'index': 'Metabolite'}, inplace=True)

    # Merge both DataFrames on 'Metabolite'
    full_parameter_table = pd.merge(parameter_table, mm_df, on='Metabolite', how='left')

    return full_parameter_table



def write_output_to_excel(model, t:TimeArray, y:ConcentrationArray, parameter_table:pd.DataFrame, file_name:str) -> None:
    '''
    Writes the output of a DynamicFBA simulation to an Excel file. The file contains three sheets:

        - 'README': Contains metadata and unit information.
        - 'Parameters': Stores the parameters used for the simulation.
        - 'Output': Tabulates metabolite concentrations over time.

    Args:
        model: A DynamicFBA model instance used to run the simulation.
        t: A time array representing the time points at which concentrations are measured.
        y: A 2D array of metabolite concentrations corresponding to each time point in t.
        parameter_table: A DataFrame containing the parameter values used in the simulation.

    Returns:
        None. The function saves an Excel file to the 'Results' directory.

    '''
    header = ['time']
    metabolite_names = list(model.pos_ex_reac.keys())
    header.extend(metabolite_names)

    output = pd.DataFrame(columns=header)
    output['time'] = t

    for conc_t, i in zip(y, range(0, len(y))):
        output.iloc[i, 1:] = conc_t

    # Save output to an excel file and include README sheet
    readme_text = {
        "README": [
            "This Excel file contains simulation results with the following parameters:",
            "Metabolite concentrations are in mmol/L, biomass in g/L.",
            "KM values are in mmol/L, Vmax values in mmol/gDW/h.",
            "See the 'Parameters' sheet for details."
        ]
    }

    readme_df = pd.DataFrame(readme_text)

    today_date = datetime.today().strftime('%Y-%m-%d')

    with pd.ExcelWriter(f"Results/{file_name}_{today_date}.xlsx", engine="openpyxl") as writer:
        readme_df.to_excel(writer, sheet_name="README", index=False)
        parameter_table.to_excel(writer, sheet_name="Parameters", index=False)
        output.to_excel(writer, sheet_name="output", index=False)

    print("Excel file saved with README and Parameter Table!")