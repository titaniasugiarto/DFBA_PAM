# display data

<h3>Das Modul 'display_data' beinhaltet Funktionen zur Darstellung
der Daten, die mit der dynamic FBA berechnet wurden. Die Daten können
als Liste oder als Plot ausgegeben werden.
___
## Imports
Zur Nutzung müssen folgende Pakete und Funktionen importiert werden:

    import matplotlib.pyplot as plt
___
## data_list_output
Hier wird die Ausgabe der Datenliste definiert. Sie soll in folgendem
Format angezeigt werden:

| Time | Metabolite 1 | Metabolite 2 | Metabolite 3 | Biomass |
|------|--------------|--------------|--------------|---------|
| 0.00 | 10.00        | 0.00         | 0.00         | 1.00    |
| 0.10 | 9.60         | 0.10         | 0.20         | 1.10    |
| 0.20 | 9.20         | 0.20         | 0.40         | 1.20    |
| 0.30 | 8.80         | 0.30         | 0.60         | 1.30    |

Dazu werden von der 'simulate'-Funktion der dFBA Klasse die Zeitschritte t, das Datenarray,
sowie die Metabolit IDs übergeben. Die oberste Tabellenzeile wird mit 'list_heading' erstellt,
indem ein String mit 'Time', den Metabolit IDs und 'Biomass' ausgegeben wird.

    def data_list_output(t, y, substrate_ids, product_ids):
        list_heading = ('Time\t' + '\t'.join(substrate_ids + product_ids) + '\tBiomass')
        print(list_heading)
    
Nachdem die Überschrift gedruckt wurde, wird eine for-Schleife über die Länge von t durchlaufen,
um die einzelnen Zeilen der Tabelle zu erstellen und auszugeben. Jede Zeile der Tabelle 
entspricht einem Zeitschritt und enthält die Konzentrationen der Substrate, Produkte und der 
Biomasse zu diesem Zeitpunkt.

Die for-Schleife iteriert über die Indizes der Zeitschritte t. Dabei wird i als Index verwendet,
um auf die einzelnen Elemente in t und den entsprechenden Reihen in y zuzugreifen.

    for i in range(len(t)):

f'{t[i]:.2f}' formatiert den aktuellen Zeitschritt auf zwei Dezimalstellen.
Der Ausdruck [f'{y[i, j]:.2f}' for j in range(len(substrate_ids) + len(product_ids) + 1)] 
erstellt eine Liste der Konzentrationen der Substrate, Produkte und der Biomasse für den 
aktuellen Zeitschritt. Auch diese Werte werden auf zwei Dezimalstellen formatiert.

'\t'.join(data_line) verbindet die Elemente der Datenzeile mit Tabulatorzeichen (\t), 
um die einzelnen Werte in Spalten darzustellen.

        data_line = [f'{t[i]:.2f}'] + [f'{y[i, j]:.2f}' for j in range(len(substrate_ids) + len(product_ids) + 1)]
        print('\t'.join(data_line))

___
## plot_data
Hier wird die grafische Darstellung der Werte in einem Plot definiert. Ein Beispielplot sieht
folgendermaßen aus:

![BeispielPlot](C:\Users\User\Desktop\MA\BeispielPlot_dFBA_package.png)

Dazu werden von der 'simulate'-Funktion der dFBA Klasse die Zeitschritte t, das Datenarray y
mit einer Dimension von 'Anzahl an Exchange Metaboliten x Zeitschritte', sowie die 
Metabolit IDs übergeben. 

    def plot_data(t, y, substrate_ids, product_ids):

Die for-Schleife iteriert über die Substrate, wobei i der Index und substrate_id 
die ID des Substrats ist. plt.plot(t, y[:, i], label=substrate_id) erstellt einen 
Plot für jedes Substrat, wobei die x-Achse die Zeit (t) und die y-Achse 
die Konzentration (y[:, i]) darstellt. Der label wird auf die ID des Substrats gesetzt, 
um eine Legende zu erstellen.

        for i, substrate_id in enumerate(substrate_ids):
            plt.plot(t, y[:, i], label=substrate_id)
        for i, product_id in enumerate(product_ids):
            plt.plot(t, y[:, len(substrate_ids) + i], label=product_id)
        plt.plot(t, y[:, -1], label='Biomasse')

Die Parameter zur Erstellung werden im Folgenden für matplotlib.pyplot definiert:

    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Dynamic FBA: Metabolite Concentrations over Time')
    plt.legend()
    plt.grid()
    plt.show()