# Utils

<h3>Hier stehen Funktionen, die nichts direkt mit der dynamic FBA zu tun haben,
allerdings trotzdem wichtig für die Datenverarbeitung sind. 
Hier werden Daten aus dem Userskript aufgenommen und verarbeitet, 
sodass sie von der dFBA Klasse genutzt werden können.

___
## Imports
Zur Nutzung müssen folgende Pakete und Funktionen importiert werden:


    from cobra.io import read_sbml_model
    import numpy as np

___
## load_model

    def load_model(path: str):  # Unterschiedliche reader einfügen
        return read_sbml_model(path)

Die Funktion 'load_model' lädt das Model aus dem Dateipfad. Der Dateipfad wird als String übergeben und das geladene cobra Model vom User im Userskript in einer Variable 'model' gespeichert. Bsp.: 

    model_path = r'C:\Users\User\Downloads\beispiel_model.xml'
    model = load_model(model_path)

___
## set_objective

    def set_objective(model, objective_id: str):
        model.objective = objective_id

Die Funktion 'set_objective' setzt die Objective Function fest. 
Übergeben werden das Model und 'objective_id', die als String vom User 
im Userskript definiert wird. Bsp.:

    set_objective(model, objective_function_id)

___
## get_exchange_metabolites
Alle ExchangeMetabolite sollen einer Position in einem Dictionary und der 
Startkonzentration (von User für beliebige Metabolite vorgegeben) in einem 1D 
np.array zugeordnet werden. Im UserScript muss das Model definiert werden:

    model = load_model(model_path)

und ein Dictionary 'start_concentrations' erstellt werden. Dort können bekannte 
Startkonzentrationen im Muster 

    start_concentrations = {'erste_ID': 10.0, 'zweite_ID: 15.0, 'dritte_ID': 20.0} 

angegeben werden. Ausgabe der Funktion sind ein Dictionary mit Metabolit 
(Exchange Reactions IDs des Models) und ihrer Position und das eindimensionale 
numpy Array 'y' mit den vorgegebenen Startkonzentrationen in der Reihenfolge 
der Positionen. Alle anderen Konzentrationen sind per default auf 0.0 gesetzt.

    def get_exchange_metabolites(model, start_concentrations):

### Erstellen des exchange_metabolites_position-Dictionary
Erstellen des Dictionarys für die Positionen zu den IDs.

    exchange_metabolites_position = {}

Geht alle ExchangeReactions im Model durch. Speichert die Reactions ID aus dem 
Model als Metabolit ID. Die Positionen im Dictionary werden eingefügt.

    for position, exchange_reaction in enumerate(model.exchanges):
        exchange_metabolite_id = exchange_reaction.id
        exchange_metabolites_position[exchange_metabolite_id] = position

### Erstellen des Numpy Arrays y mit Startkonzentrationen
Das numpy Array 'y' wird erstellt und in der Länge der Exchange-Metabolitanzahl 
mit Nullen (Defaultwert) aufgefüllt.

    y = np.zeros(shape=len(exchange_metabolites_position))

Das vom User erstellte Dictionary 'start_concentrations' wird durchgegangen. 
Dann wird überprüft, ob die vom User angegebenen IDs im Model vorhanden sind. 
Dann wird zur ID die passende Position herausgesucht. Diese Position (int) wird 
als Stelle in y genutzt um den ersten Wert auf die Startkonzentration zu setzen.

    for metabolite, start_concentration in start_concentrations.items():
        if metabolite in exchange_metabolites_position:
            position = exchange_metabolites_position[metabolite]
            y[position] = start_concentration

Das Dictionary 'exchange_metabolites_position' und das numpy Array y werden 
von der Funktion zurückgegeben.
    
    return exchange_metabolites_position, y
