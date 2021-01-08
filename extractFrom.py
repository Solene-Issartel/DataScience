from pandas import *
import numpy as np
from sklearn.decomposition import PCA
import plotly.express as px
import matplotlib.pyplot as plt

# Récupérer les thématiques associées à un mail
def retrieve_thematiques(stringToChange):
    wordsAssociated = stringToChange
    wordsAssociated = wordsAssociated.replace("[", "")
    wordsAssociated = wordsAssociated.replace("]", "")
    wordsAssociated = wordsAssociated.replace(",", "")
    wordsAssociated = wordsAssociated.replace("'", "")
    wordsAssociated = wordsAssociated.split(" ")
    return wordsAssociated


def extract_data(csv_file):
    df = pandas.read_csv(csv_file, low_memory=False, header=0)
    df = df[['From', 'Thematiques']]
    thematiques = []
    for row in df['Thematiques']:
        thematiques.append(retrieve_thematiques(row))
    df['Thematiques'] = thematiques
    new_df = df.groupby(['From'], sort=False)['Thematiques'].apply(lambda x: x.sum())
    list_dic = []
    for personne in new_df:
        compte = {k: personne.count(k) for k in set(personne)}
        list_dic.append(compte)

    mails_df = df.groupby(['From'], sort=False).count()
    mails_df["Dictionnaire des thématiques"] = list_dic
    mails_df = mails_df.query('Thematiques>=50')
    mails_df = mails_df.rename(columns={"Thematiques": "Nombre d\'emails envoyés"})
    print(mails_df)
    return mails_df


# Return le tableau de contingence sur lequel on déroulera l'AFC
# Les expéditeurs et les thématiques de leurs mails envoyés
def tableauAFC(dataframe):
    df1 = pandas.read_csv("visualisation/data/clean_thematiques.csv", low_memory=False, header=0)
    columns = []
    # Une ligne vide, qui va ensuite prendre les thématiques associées à l'expéditeur
    emptyRow = []
    # On récupère les différentes thématiques
    for thematiques in df1["mainThematique"]:
        emptyRow.append(0)
        columns.append(thematiques)
    # les expéditeurs avec leurs thématiques
    expThematiques = pandas.DataFrame(columns=columns)
    list_exp = []
    # Pour chaque expéditeur
    for expediteur in dataframe.iterrows():
        dico = expediteur[1][1]
        # On crée une nouvelle ligne avec des 0
        newExpRow = emptyRow
        # On en fait un dataframe comprenant toutes les colonnes voulues
        newExpRow = pandas.DataFrame(data=np.array([newExpRow]), columns=columns)
        # On indique qui est l'expéditeur
        list_exp.append(expediteur[0])
        # On met à jour ses thématiques selon le dictionnaire de ses thématiques
        for key, value in dico.items():
            newExpRow[key] = value
        # Puis on ajoute notre expediteur avec ses thématiques dans le dataframe
        expThematiques = pandas.concat([expThematiques, newExpRow], ignore_index=True)
    # On a fini d'attribuer les différentes thématiques aux expéditeurs
    expThematiques.index = list_exp
    print(expThematiques)
    return expThematiques


def plot_factor_variable():
    plt.figure(figsize=(10, 10))
    plt.rcParams.update({'font.size': 14})

    #
    x = np.linspace(start=-1, stop=1, num=500)
    y_positive = lambda x: np.sqrt(1 - x ** 2)
    y_negative = lambda x: -np.sqrt(1 - x ** 2)
    plt.plot(x, list(map(y_positive, x)), color='maroon')
    plt.plot(x, list(map(y_negative, x)), color='maroon')

    x = np.linspace(start=-0.5, stop=0.5, num=500)
    y_positive = lambda x: np.sqrt(0.5 ** 2 - x ** 2)
    y_negative = lambda x: -np.sqrt(0.5 ** 2 - x ** 2)
    plt.plot(x, list(map(y_positive, x)), color='maroon')
    plt.plot(x, list(map(y_negative, x)), color='maroon')

def afc(tabAFC):
    # On transforme notre tableau en matrice
    x = tabAFC.values
    pca = PCA(n_components=66)
    pca.fit(x)
    # Donne les vecteurs des valeurs propres
    coord = pca.components_
    # Donne les valeurs propres
    eigenvalues = pca.explained_variance_ratio_
    # La plupart des valeurs propres est très petite, on garde seulement
    # les plus grandes
    filter_arr = eigenvalues > 0.01
    eigenvalues = eigenvalues[filter_arr]
    print(eigenvalues)
    # Diagramme en barre des valeurs propres
    fig = px.bar(eigenvalues)
    fig.show()


if __name__ == '__main__':
    df = extract_data("visualisation/data/mails_thematiques.csv")
    df = tableauAFC(df)
    afc(df)
