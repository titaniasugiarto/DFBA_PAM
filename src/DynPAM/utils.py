import os
import pickle
import numpy as np
from cobra.io import read_sbml_model


def load_model(path: str):
    extension = os.path.splitext(path)[1].lower().strip()
    if extension == '.pkl':
        with open(path, "rb") as f:
            model = pickle.load(f)
            print('Model loadad.')
        return model
    elif extension in ['.xml', '.sbml']:
        model = read_sbml_model(path)
        print('Model loadad.')
        return model
    else:
        raise ValueError(f"Unsupported file extension: {extension}. Supported extensions are .pkl, .xml, .sbml.")


def set_objective(model, objective_function_id: str):
    model.objective = objective_function_id
    print('Objective function is set.')


# Erstellt Dictionary mit ex_reac_ID als key und fortlaufende Nummer als Value
def position_exchange_reactions(model, objective_function_id: str):
    dict_position_ex_reaction = {}
    position = 0
    for exchange_reaction in model.exchanges:
        exchange_reaction_id = exchange_reaction.id
        dict_position_ex_reaction[exchange_reaction_id] = position
        position += 1

    dict_position_ex_reaction[objective_function_id] = position

    return dict_position_ex_reaction

# Erstellt Dictionary mit enzyme_ID als key und fortlaufende Nummer als Value
def position_enzymes(model):
    dict_position_enzymes = {}
    position = 0
    for enzyme in model.reactions:
        enzyme_id = enzyme.id
        dict_position_enzymes[enzyme_id] = position
        position += 1

    return dict_position_enzymes


def set_start_concentrations_metabolites(start_concentrations_metabolites, position_exchange_reactions):
    y0 = np.zeros(len(position_exchange_reactions))

    for reac_id, concentration in start_concentrations_metabolites.items():
        if reac_id in position_exchange_reactions:
            y0[position_exchange_reactions[reac_id]] = concentration
        else:
            print(f"Warning: Metabolite {reac_id} not found in position mapping.")

    return y0


def set_start_concentrations_enzymes(start_concentrations_enzymes, dict_position_enzymes):
    e0 = np.zeros(len(dict_position_enzymes))

    for enzyme_id, concentration in start_concentrations_enzymes.items():
        if enzyme_id in dict_position_enzymes:
            e0[dict_position_enzymes[enzyme_id]] = concentration
        else:
            print(f"Warning: Enzyme {enzyme_id} not found in position mapping.")

    return e0

def set_start_concentrations(start_concentrations, pos_ex_reac, pos_enzymes):
    """
    Sets the initial concentrations for metabolites and enzymes by combining 
    set_start_concentrations_metabolites and set_start_concentrations_enzymes.
    """
    y0 = set_start_concentrations_metabolites(start_concentrations.get('metabolites', {}), pos_ex_reac)
    e0 = set_start_concentrations_enzymes(start_concentrations.get('enzymes', {}), pos_enzymes)
    
    # Combine both metabolite and enzyme concentrations
    return np.concatenate((y0, e0))
