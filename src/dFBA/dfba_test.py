from dynamic_fba import DynamicFBA
from display_data import (data_list_output, 
                          plot_data)
from utils import (load_model,
                   set_objective,
                   position_exchange_reactions,
                   set_start_concentrations)

model = load_model(r"C:\Users\User\Documents\GitHub\dyn-pam\Models\e_coli_core.xml")

print("Model loadad.")

set_objective(model, "BIOMASS_Ecoli_core_w_GAM")

print("Objective set.")


