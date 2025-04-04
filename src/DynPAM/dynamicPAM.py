import numpy as np
from cobra import Model
from src.DynPAM.utils import position_enzymes, set_start_concentrations_enzymes, position_exchange_reactions, set_start_concentrations_metabolites
from src.DynPAM.display_data import plot_data, data_list_output
from assimulo.problem import Explicit_Problem
from assimulo.solvers import ExplicitEuler
from assimulo.exception import TerminateSimulation

class DynamicPAM:
    def __init__(self, model: Model, max_production, max_degradation, michaelis_menten_parameters: dict, objective_function_id: str, start_concentrations: dict):
        
        self.model = model
        self.objective_function_id = objective_function_id

        self.max_production = max_production
        self.max_degradation = max_degradation
        self.michaelis_menten_parameters = michaelis_menten_parameters

        # two dicts are made, one for positions of ex_reac_IDs and one for enzyme_IDs
        self.pos_ex_reac = position_exchange_reactions(model, objective_function_id)
        self.dict_position_enzymes = position_enzymes(model)
        
        # start concentrations for ex_met are set in an np Array y0
        self.start_concentrations_ex_met = set_start_concentrations_metabolites(start_concentrations['metabolites'], self.pos_ex_reac)
        self.start_concentrations_enz = set_start_concentrations_enzymes(start_concentrations['enzymes'], self.dict_position_enzymes)

        self.e = np.zeros(len(self.dict_position_enzymes)) # Vektor für enzyme konz.


    # Function to set the lower bounds of the ex metabolites using michaelis menten parameters
    def set_ex_met_bounds(self, y):
        for reaction_id, parameter in self.michaelis_menten_parameters.items():
            position = self.pos_ex_reac[reaction_id]
            metabolite_concentration = y[position]

            metabolite_reaction = ((parameter['Vmax'] * metabolite_concentration) /
                                   (parameter['KM'] + metabolite_concentration))

            if metabolite_reaction < 0:
                metabolite_reaction = 0

            self.model.reactions.get_by_id(reaction_id).lower_bound = -metabolite_reaction


    def provide_start_concentrations(self, concentrations):  

        e = concentrations[:len(self.dict_position_enzymes)]
        y = concentrations[len(self.dict_position_enzymes):] 

        self.set_ex_met_bounds(self, y)
        
        solution = self.model.optimize()
        if solution.status != 'optimal':
            raise RuntimeError(f"Optimization failed with status: {solution.status}")
        
        self.e = e


    def rhs(self, t, concentrations):
        d_concentration_dt = np.zeros(len(concentrations))

        # Separate enzyme concentrations and metabolite concentrations
        e = concentrations[:len(self.dict_position_enzymes)]
        y = concentrations[len(self.dict_position_enzymes):]

        # Ensure non-negative enzyme concentrations
        # for i in range(len(e)):
        #     if e[i] < 0:
        #         e[i] = 0
        e = np.maximum(e, 0)

        # Update enzyme reaction bounds
        for enzyme_id in self.dict_position_enzymes:
            position = self.dict_position_enzymes[enzyme_id]
            enzyme_concentration = e[position]

            l_bound = enzyme_concentration + self.max_degradation
            u_bound = enzyme_concentration + self.max_production

            self.model.reactions.get_by_id(enzyme_id).lower_bound = l_bound
            self.model.reactions.get_by_id(enzyme_id).upper_bound = u_bound

        biomass = y[self.pos_ex_reac[self.objective_function_id]]

        # Ensure non-negative metabolite concentrations
        # for i in range(len(y)):
        #     if y[i] < 0:
        #         y[i] = 0
        y = np.maximum(y, 0)

        self.set_ex_met_bounds(y)

        # Optimize the model
        solution = self.model.optimize()

        if solution.status != 'optimal':
            raise RuntimeError(f"Optimization failed with status: {solution.status}")

        # Update enzyme concentration changes
        for enzyme_id, position in self.dict_position_enzymes.items():
            flux = solution.fluxes[enzyme_id]
            d_concentration_dt[position] = flux #*10^6

        # Update metabolite concentration changes
        for reac_id, pos in self.pos_ex_reac.items():
            flux = solution.fluxes[reac_id]
            d_concentration_dt[len(self.dict_position_enzymes) + pos] = flux * biomass

        return d_concentration_dt

    def simulate(self, t0: float, tf: float, start_concentrations: dict, data_list: bool = True, plot: bool = True, plot_ids=None, exclude_ids=None, only_positive=False, plot_biomass_separately=True):
        e0 = set_start_concentrations_enzymes(start_concentrations, self.dict_position_enzymes)
        y0 = self.start_concentrations_ex_met      
        initial_conditions = np.concatenate((e0, y0))

        problem = Explicit_Problem(self.rhs, initial_conditions, t0)
        solver = ExplicitEuler(problem)

        try:
            t, concentrations = solver.simulate(tf) # concentrations ist nur metabolite, nicht enzymes
        except TerminateSimulation:
            pass

        e = concentrations[:, :len(self.dict_position_enzymes)]
        y = concentrations[:, len(self.dict_position_enzymes):]

        if data_list:
            data_list_output(t, e, self.dict_position_enzymes)
            data_list_output(t, y, self.pos_ex_reac)

        if plot:
            
            plot_data(t, e, self.dict_position_enzymes, exclude_ids=exclude_ids, plot_ids=plot_ids, only_positive=only_positive)
            plot_data(t, y, self.pos_ex_reac, exclude_ids=exclude_ids, plot_ids=plot_ids, only_positive=only_positive)

        return t, concentrations
