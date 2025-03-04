import matplotlib.pyplot as plt

def plot_data(t, y, pos_ex_reac, metabolite_ids, biomass_id, enzyme_ids, exclude_ids=None, plot_ids=None, only_positive=False):
    if exclude_ids:
        metabolite_ids = [mid for mid in metabolite_ids if mid not in exclude_ids]
        enzyme_ids = [eid for eid in enzyme_ids if eid not in exclude_ids]
    
    if plot_ids:
        metabolite_ids = [mid for mid in metabolite_ids if mid in plot_ids]
        enzyme_ids = [eid for eid in enzyme_ids if eid in plot_ids]
    
    # Plot Metabolite Concentrations
    plt.figure(figsize=(12, 4))
    for met_id in pos_ex_reac:
        if met_id in pos_ex_reac:
            pos = pos_ex_reac[met_id]
            concentrations = y[:, pos]
            if only_positive:
                concentrations = concentrations[concentrations >= 0]
            plt.plot(t, concentrations, label=met_id)
    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Metabolite Concentrations Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Plot Biomass
    plt.figure(figsize=(12, 4))
    if biomass_id in pos_ex_reac:
        biomass_pos = pos_ex_reac[biomass_id]
        biomass_concentrations = y[:, biomass_pos]
        if only_positive:
            biomass_concentrations = biomass_concentrations[biomass_concentrations >= 0]
        plt.plot(t, biomass_concentrations, label=biomass_id)
        plt.xlabel('Time')
        plt.ylabel('Concentration')
        plt.title('Biomass Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    # Plot Enzyme Concentrations
    plt.figure(figsize=(12, 4))
    for enzyme_id in enzyme_ids:
        if enzyme_id in pos_ex_reac:
            pos = pos_ex_reac[enzyme_id]
            concentrations = y[:, pos]
            if only_positive:
                concentrations = concentrations[concentrations >= 0]
            plt.plot(t, concentrations, label=enzyme_id)
    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Enzyme Concentrations Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def data_list_output(t, y, pos_ex_reac):
    enzyme_ids = list(pos_ex_reac.keys())
    
    print("Time points:", t)
    for enzyme_id in enzyme_ids:
        pos = pos_ex_reac[enzyme_id]
        concentrations = y[:, pos]
        print(f"Concentrations for {enzyme_id}: {concentrations}")