from src.DynPAM.dynamicPAM import DynamicPAM
from src.DynPAM.utils import load_model, set_objective, set_start_concentrations_metabolites, position_enzymes, set_start_concentrations_enzymes, position_exchange_reactions, set_start_concentrations
from src.DynPAM.display_data import data_list_output, plot_data
from PAModelpy.utils.pam_generation import set_up_pam
import numpy as np

model_path = 'Data/proteinAllocationModel_mciML1515_EnzymaticData_multi.xlsx'
model = set_up_pam(model_path, sensitivity=False)

objective_function_id = 'BIOMASS_Ec_iML1515_WT_75p37M'
set_objective(model, objective_function_id)

# Define start concentrations for enzymes and metabolites
start_concentrations_enzymes = {
    'ENO': 0.1,
    'PYK': 0.1,
    'PFL': 0.1
}

start_concentrations_metabolites = {
    'EX_glc__D_e': 1.0,
    'EX_o2_e': 0.5,
    'EX_ac_e': 0.1
}

# Get position mappings
pos_ex_reac = position_exchange_reactions(model, objective_function_id)
pos_enzymes = position_enzymes(model)
pos_biomass = pos_ex_reac[objective_function_id]

# # Set initial concentrations
# y0 = set_start_concentrations_metabolites(start_concentrations_metabolites, pos_ex_reac)
# e0 = set_start_concentrations_enzymes(start_concentrations_enzymes, pos_enzymes)
# initial_concentrations = np.concatenate((e0, y0))

start_concentrations = {
    'metabolites': {
        'EX_glc__D_e': 1.0,
        'EX_o2_e': 0.5,
        'EX_ac_e': 0.1
    },
    'enzymes': {
        'ENO': 0.1,
        'PYK': 0.1,
        'PFL': 0.1
    }
}

# Initiale Konzentrationen setzen
y0 = set_start_concentrations(start_concentrations, pos_ex_reac, pos_enzymes)
e0 = y0

# Initialize DynamicPAM instance
dynamic_pam = DynamicPAM(model,
                         max_production=10,
                         max_degradation=-5,
                         michaelis_menten_parameters={},
                         objective_function_id=objective_function_id,
                         start_concentrations=start_concentrations
                         )

# Run the simulation
t0 = 0
tf = 0.3
t, y = dynamic_pam.simulate(t0, tf, start_concentrations, plot=True, only_positive=True) # Variable

# # Stelle sicher, dass enzyme_ids und biomass_id korrekt als Listen übergeben werden
# enzyme_ids = list(dynamic_pam.dict_position_enzymes.keys())  # Liste der Enzym-IDs
# biomass_id = [pos_ex_reac[objective_function_id]]  # Biomasse-ID als Liste, auch wenn es nur ein einziges Element ist
#
# # Plot the results
# plot_data(t, y, dynamic_pam.pos_ex_reac, pos_biomass, biomass_id, enzyme_ids)  # biomass_id als Liste
#
# # Print the data list output
# data_list_output(t, y, pos_ex_reac, pos_biomass, pos_enzymes)