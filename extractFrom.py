from pandas import *
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
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
def tableau_acp(dataframe):
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


def acp(tab_acp):
    columns = tab_acp.columns.values
    X = tab_acp
    # nombre d'observations
    n = X.shape[0]
    # nombre de variables
    p = X.shape[1]
    # instanciation
    sc = StandardScaler()
    # transformation – centrage
    Z = sc.fit_transform(X)
    acp = PCA(svd_solver='full')
    coord = acp.fit_transform(Z)
    eigenvalues = acp.explained_variance_ratio_[:10]
    eigEx = acp.explained_variance_
    plot_valeurs_propres(eigenvalues)
    plot_factor_variable2(X,eigEx,eigenvalues,n,p,acp)

# Diagramme en barre des valeurs propres
def plot_valeurs_propres(eigenvalues):
    fig = px.bar(eigenvalues)
    fig.show()


def nuages_individus1(tablePCA):
    sc = StandardScaler()  # transformation–centrage-réduction
    Z = sc.fit_transform(tablePCA)
    print(Z)
    acpp = PCA(n_components=10)
    coord = acpp.fit_transform(Z)

    #positionnement des individus dans lepremier plan
    fig, axes = plt.subplots(figsize=(15,15))
    axes.set_xlim(-4,33) #même limites en abscisse
    axes.set_ylim(-4,20) #et en ordonnée
    # #placement des étiquettes des observations
    n=66
    for i in range(n):
        plt.annotate(tablePCA.index[i],(coord[i,0],coord[i,1]))#ajouter les axes
    plt.plot([-4,33],[0,0],color='silver',linestyle='-',linewidth=1)
    plt.plot([0,0],[-4,33],color='silver',linestyle='-',linewidth=1)#affichage
    plt.show()

def nuages_individus(tabAFC):
    columns = tabAFC.columns.values
    # Centré et réduire les données
    scaler = StandardScaler()
    scaler.fit(tabAFC)
    Z = scaler.transform(tabAFC)

    # ACP
    acp = PCA(n_components=10)
    coord = acp.fit_transform(Z)
    acp.fit(Z)
    results = acp.fit_transform(Z)
    # #placement des étiquettes des observations
    n = 66
    for i in range(n):
        plt.annotate(tabAFC.index[i], (coord[i, 0], coord[i, 1]))  # ajouter les axes
    plt.scatter(coord[:, 0], coord[:, 1])
    plt.show()


# Nuage des variables
def plot_factor_variable2(X,eigEx,eigenvalues,n,p,acp):
    eigval = (n - 1) / n * eigEx
    sqrt_eigval = np.sqrt(eigval)
    corvar = np.zeros((p, p))
    for k in range(p):
        corvar[:, k] = acp.components_[k, :] * sqrt_eigval[k]

    # cercle des corrélations
    fig, axes = plt.subplots(figsize=(8, 8))
    axes.set_xlim(-1, 1)
    axes.set_ylim(-1, 1)
    # affichage des étiquettes (noms des variables)
    for j in range(p):
        plt.arrow(0, 0,
                  dx=corvar[j, 0], dy=corvar[j, 1],
                  head_width=0.03, head_length=0.03,
                  length_includes_head=True)
        plt.annotate(X.columns[j], (corvar[j, 0], corvar[j, 1]))

    # ajouter les axes
    plt.plot([-1, 1], [0, 0], color='silver', linestyle='-', linewidth=1)
    plt.plot([0, 0], [-1, 1], color='silver', linestyle='-', linewidth=1)

    # ajouter un cercle
    cercle = plt.Circle((0, 0), 1, color='black', fill=False)
    axes.add_artist(cercle)

    plt.xlabel(f"Dim 1 ({round(eigenvalues[0] * 100,2)}%)")
    plt.ylabel(f"Dim 2 ({round(eigenvalues[1] * 100,2)}%)")
    plt.title('Variable factor map (PCA)')
    # affichage
    plt.show()

if __name__ == '__main__':
    df = extract_data("visualisation/data/mails_thematiques.csv")
    df = tableau_acp(df)
    df.to_csv("visualisation/data/extracted_data.csv")
    nuages_individus1(df)
    acp(df)
