import numpy as np
from assimulo.problem import Explicit_Problem
from assimulo.solvers import RungeKutta34
from assimulo.solvers import ExplicitEuler
from assimulo.exception import TerminateSimulation
from cobra import Model
from display_data import plot_data
from display_data import data_list_output
from utils import (position_exchange_reactions,
                    set_start_concentrations)


class DynamicFBA:
    def __init__(self,
                 model: Model,
                 michaelis_menten_parameters: dict,
                 objective_function_id: str):
        
        self.model = model
        self.michaelis_menten_parameters = michaelis_menten_parameters
        self.objective_function_id = objective_function_id
        self.pos_ex_reac = {} # position of component in y

    def rhs_definition(self, t, y):

        d_metabolite_dt = np.zeros(len(y))
        biomass = y[self.pos_ex_reac[self.objective_function_id]]

        # Berechnung der Änderungsraten und Anpassung der Flussgrenzen
        for reaction_id, parameter in self.michaelis_menten_parameters.items():
            # get metabolte concetration
            position = self.pos_ex_reac[reaction_id]
            metabolite_concentrations = y[position]

            for i in range(len(y)):
                if y[i] < 0:
                    y[i] = 0

            # calculate metabolite flux
            metabolite_reaction = ((parameter['Vmax'] * metabolite_concentrations) /
                                   (parameter['KM'] + metabolite_concentrations))

            if metabolite_reaction < 0:
                metabolite_reaction = 0

            # self.model.reactions.get_by_id(reaction_id).upper_bound = 100
            self.model.reactions.get_by_id(reaction_id).lower_bound = -metabolite_reaction

        solution = self.model.optimize()

        if solution.status != 'optimal':
           raise RuntimeError(f"Optimization failed with status: {solution.status}")

        for reac_id, pos in self.pos_ex_reac.items():
            flux = solution.fluxes[reac_id]
            d_metabolite_dt[pos] = flux * biomass

        return d_metabolite_dt #mmol/h

    def simulate(self, t0: float, tf: float, start_concentrations: dict,
                 data_list: bool = True, plot: bool = True, plot_ids=None, exclude_ids=None, only_positive=False, plot_biomass_separately=False):
        
        # initialize problem and populate start concentration vector
        self.pos_ex_reac = position_exchange_reactions(self.model, self.objective_function_id)
        y0 = set_start_concentrations(start_concentrations, self.pos_ex_reac)

        problem = Explicit_Problem(self.rhs_definition, y0, t0)
        # solver = RungeKutta34(problem)
        solver = ExplicitEuler(problem)
        # Sets the initial step, default is 0.01
        # solver.inith = 0.1

        try:
            t, y = solver.simulate(tf)
        except TerminateSimulation:
            pass

        if data_list:
            data_list_output(t, y, self.pos_ex_reac)
        if plot:
            plot_data(t, y, 
                      self.pos_ex_reac, 
                      exclude_ids=exclude_ids, 
                      plot_ids=plot_ids,
                      only_positive=only_positive, 
                      plot_biomass_separately=plot_biomass_separately)

        return t, y  # t 1D np array, y 2D np array y[i, j]
