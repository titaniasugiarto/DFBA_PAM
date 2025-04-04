from src.dFBA.dynamic_fba import DynamicFBA
from src.dFBA.display_data import (data_list_output,
                          plot_data)
from src.dFBA.utils import (load_model,
                   set_objective,
                   position_exchange_reactions,
                   set_start_concentrations,
                   create_parameter_table)
import pandas as pd
from datetime import datetime

model = load_model(r"Models/e_coli_core.xml")

print("Model loadad.")

biomass_reaction_core = "BIOMASS_Ecoli_core_w_GAM"
objective_function_id = biomass_reaction_core
set_objective(model, biomass_reaction_core)

print("Objective set.")

start_concentrations = {'EX_glc__D_e': 92.0, #all concentrations in mmol/L
                        'EX_ac_e': 2.0,
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

print("MM parameters given.")

dynamic_fba = DynamicFBA(model,
                         michaelis_menten_parameters,
                         objective_function_id)

print("DynamicFBA initialized.")

t0 = 0.0  # Startzeit
tf = 6  # Endzeit
plot_ids = ['EX_glc__D_e', 'EX_ac_e', biomass_reaction_core]
t, y = dynamic_fba.simulate(t0, tf, start_concentrations,
                            data_list=False, plot=False, plot_ids=plot_ids)

header = ['time']
metabolite_names= list(dynamic_fba.pos_ex_reac.keys())
header.extend(metabolite_names)

output = pd.DataFrame(columns=header)
output['time'] = t

for conc_t, i  in zip(y, range(0,len(y))):
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

with pd.ExcelWriter(f"Results/dfba_{today_date}.xlsx", engine="openpyxl") as writer:
    readme_df.to_excel(writer, sheet_name="README", index=False)
    parameter_table.to_excel(writer, sheet_name="Parameters", index=False)
    output.to_excel(writer, sheet_name="output", index=False)

print("Excel file saved with README and Parameter Table!")

