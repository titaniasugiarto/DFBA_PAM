# dynamic FBA
<h3>Das Modul dynamic_fba beinhaltet Funktionen zur Durchführung 
von dynamischen Flussbilanzanalysen (FBA). Diese Analysen 
simulieren die zeitabhängige Veränderung von 
Metabolitenkonzentrationen in einem biochemischen Netzwerk.
___
## Imports
Zur Nutzung müssen folgende Pakete und Funktionen importiert werden:

    import numpy as np
    from assimulo.problem import Explicit_Problem
    from assimulo.solvers import RungeKutta34
    from assimulo.exception import TerminateSimulation
    from cobra import Model
    from .display_data import data_list_output, plot_data
___
## DynamicFBA
Die Klasse DynamicFBA implementiert die dynamische FBA.

    class DynamicFBA:

## Initialisierung
Die Initialisierung der Parameter erfolgt im Konstruktor der Klasse:

    def __init__(self,
                 model: Model,
                 initial_concentrations: dict,
                 km: dict,
                 vmax: dict,
                 substrate_id: list,
                 objective_function_id: str,
                 y):

- model (Model): Das biochemische Modell.
- initial_concentrations (dict): Ein Dictionary mit den initialen Konzentrationen der Metaboliten.
- km (dict): Ein Dictionary mit den Michaelis-Menten-Konstanten.
- vmax (dict): Ein Dictionary mit den maximalen Reaktionsgeschwindigkeiten.
- substrate_id (list): Eine Liste der IDs der Substrate.
- objective_function_id (str): Die ID der Zielreaktion.
- y (numpy.ndarray): Ein Numpy-Array der initialen Konzentrationen.

        self.model = model
        self.km = km  # K(M) [mmol*L-1]
        self.vmax = vmax  # V(max) [mmol * (L * h)-1]
        self.initial_concentrations = initial_concentrations  # concentrations [mmol * L-1]
        self.substrate_ids = substrate_id
        self.objective_function_id = objective_function_id
        self.y = y

        self.exchange_ids = [r.id for r in model.exchanges]
        self.product_ids = list(set(self.exchange_ids) - set(self.substrate_ids))

- self.model, self.km, self.vmax, self.initial_concentrations, self.substrate_ids, 
self.objective_function_id und self.y speichern die übergebenen Parameter.
- self.exchange_ids enthält die IDs der Austauschreaktionen im Modell.
- self.product_ids enthält die IDs der Produkte (alle Austauschreaktionen außer den Substraten).
___
## Definition der Differentialgleichungen
Die Methode rhs_definition definiert die rechte Seite der Differentialgleichungen, 
die die zeitliche Änderung der Metabolitenkonzentrationen beschreiben.

    def rhs_definition(self, t, y):
        d_substrate_dt = np.zeros(len(self.substrate_ids))  # [mol * L-1]
        # d_product_dt = np.zeros(len(self.product_ids))  # [mol * L-1]
        biomass = y[-1]  # growth rate [gCDW * L-1]

        # Neu, für mehrere Substrate
        for i, substrate_id in enumerate(self.substrate_ids):
            substrate_concentrations = y[i]
            substrate_reaction = ((self.vmax[substrate_id] * substrate_concentrations) / (self.km[substrate_id] + substrate_concentrations))  # Aufnahmerate in Zelle [mmol * (L * h)-1] # lambda function
            d_substrate_dt[i] = - substrate_reaction * biomass
            # Bounds von Reaktionen werden definiert
            self.model.reactions.get_by_id(substrate_id).upper_bound = 0.0
            self.model.reactions.get_by_id(substrate_id).lower_bound = - substrate_reaction

        # Perform FBA to get the fluxes
        solution = self.model.optimize()
        growth_rate = solution.fluxes[self.objective_function_id]  # ['BIOMASS_Ecoli_core_w_GAM']  # [gCDW * gCDW-1 * h-1]

        '''for i, product_id in enumerate(self.product_ids):
            secretion_rate = solution.fluxes[product_id]
            d_product_dt[i] = secretion_rate * biomass'''

        d_biomass_dt = biomass * growth_rate  # [gCDW * L-1] * [gCDW * gCDW-1 * h-1] = [gCDW * L-1 * h-1]

        return np.concatenate(d_substrate_dt, d_biomass_dt)

    def simulate(self, t0: float, tf: float, data_list: bool = True, plot: bool = True):
        # Initialize problem for the solver
        initial_conditions = [self.initial_concentrations[met_id] for met_id in self.substrate_ids + self.product_ids] + [self.initial_concentrations['objective_function']]
        problem = Explicit_Problem(self.rhs_definition, initial_conditions, t0)
        solver = RungeKutta34(problem)

        # Simulate and handle exception
        try:
            t, y = solver.simulate(tf)
        except TerminateSimulation:
            pass

        if data_list:
            data_list_output(t, y, self.substrate_ids, ['Biomass'])
        if plot:
            plot_data(t, y, self.substrate_ids, ['Biomass'])

        return t, y
