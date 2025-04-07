from src.dFBA.dynamic_fba import DynamicFBA
from src.dFBA.display_data import (data_list_output,
                          plot_data)
from src.dFBA.utils import (load_model,
                   set_objective,
                   position_exchange_reactions,
                   set_start_concentrations,
                   create_parameter_table)
from PAModelpy.utils.pam_generation import set_up_pam

pam_path = 'Data/proteinAllocationModel_mciML1515_EnzymaticData_multi.xlsx'
model = set_up_pam(pam_path, sensitivity=False)
# model = load_model('Models/iML1515.xml')

print("Model loadad.")

biomass_reaction_core = "BIOMASS_Ec_iML1515_core_75p37M"
objective_function_id = biomass_reaction_core
set_objective(model, biomass_reaction_core)

print("Objective set.")

start_concentrations = {'EX_glc__D_e': 92.0, #all concentrations in mmol/L
                        'EX_ac_e': 0.1,
                        #'EX_etoh_e': 1.0,
                        #'EX_lac__D_e': 5.0,
                        biomass_reaction_core: 0.1}
print("Concentrations given.")

michaelis_menten_parameters = {'EX_glc__D_e': {'KM': 0.0027, 'Vmax': 10.5}, # K(M) [mmol*L-1], V(max) [mmol * (L * h)-1]
                               'EX_ac_e': {'KM': 0.02, 'Vmax': 8.0},
                               #'EX_etoh_e': {'KM': 0.017, 'Vmax': 9.0},
                               #'EX_lac__D_e': {'KM': 0.015, 'Vmax': 10.0}
                               }

# Create a table with the simulation's parameters
parameter_table = create_parameter_table(start_concentrations, michaelis_menten_parameters)
print(parameter_table)

print("MM parameters given.")

dynamic_fba = DynamicFBA(model=model,
                         michaelis_menten_parameters=michaelis_menten_parameters,
                         objective_function_id=objective_function_id,
                         parameter_table=parameter_table)

print("DynamicFBA initialized.")

t0 = 0.0  # Startzeit
tf = 13  # Endzeit
plot_ids = ['EX_glc__D_e', 'EX_ac_e', biomass_reaction_core]
t, y = dynamic_fba.simulate(t0, tf, start_concentrations,
                            data_list=False, plot=True, plot_ids=plot_ids, save_output=False)



