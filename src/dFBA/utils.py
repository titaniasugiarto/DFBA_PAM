from cobra.io import read_sbml_model
import numpy as np
import pickle
import os

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
