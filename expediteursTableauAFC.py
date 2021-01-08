from pandas import *
import numpy as np
from fanalysis.ca import CA

# Return le tableau de contingence sur lequel on déroulera l'AFC
# Les expéditeurs et les thématiques de leurs mails envoyés
def tableauAFC(dataframe):
    df1 = pandas.read_csv("visualisation/data/clean_thematiques.csv", low_memory=False, header=0)
    columns = [""]
    # Une ligne vide, qui va ensuite prendre les thématiques associées à l'expéditeur
    emptyRow = [0]
    # On récupère les différentes thématiques
    for thematiques in df1["mainThematique"]:
        emptyRow.append(0)
        columns.append(thematiques)
    # les expéditeurs avec leurs thématiques
    expThematiques = pandas.DataFrame(columns=columns)
    # Pour chaque expéditeur
    for expediteur in dataframe.itterows:
        # On crée une nouvelle ligne avec des 0
        newExpRow = emptyRow
        # On en fait un dataframe comprenant toutes les colonnes voulues
        newExpRow = pandas.DataFrame(data=np.array([newExpRow]), columns=columns)
        # On indique qui est l'expéditeur
        newExpRow[""] = expediteur[0]
        # On met à jour ses thématiques selon le dictionnaire de ses thématiques
        for key, value in dataframe[2].iteritems():
            print(key)
            print(value)
            newExpRow[key] = value
        # Puis on ajoute notre expediteur avec ses thématiques dans le dataframe
        expThematiques = pandas.concat([expThematiques, newExpRow], ignore_index=True)
    # On a fini d'attribuer les différentes thématiques aux expéditeurs
    print(expThematiques)
    return expThematiques


def AFC(tabAFC):
    # On transforme notre tableau en matrice
    X = tabAFC.as_matrix()
    my_ca = CA(row_labels=tabAFC.index.values, col_labels=tabAFC.columns.values)
    # On réalise l'AFC
    my_ca.fit(X)
    # Les valeurs propres
    print(my_ca.eig_)
    my_ca.plot_eigenvalues()

if __name__ == '__main__':
    print("Hello !")
