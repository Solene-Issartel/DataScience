from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from pandas import *
import time

def create_thematiques(col,df):
    start_time = time.time()
    # La liste qui contiendra les thématiques avec leurs mots associées
    thematiques = []
    # Pour chaque mot récupéré dans les subjects
    for motBrut in df[col]:
        # On enlève les mots au pluriel
        mot =  WordNetLemmatizer().lemmatize(motBrut)
        exist = False
        count = 0
        # On regarde si on a déjà eu ce mot dans les mots proches précédents
        while (count < len(thematiques) and exist == False):
            if (mot in thematiques[count]):
                exist = True
            else:
                count += 1
        # On récupère les mots en commun si on ne l'a pas déjà traité
        closeWords = wordnet.synsets(mot)
        if (exist):
            # Mot déjà traité, on les rajoute dans la bonne case
            for cws in closeWords:
                # On regarde si la liste du mot proche contient le mot cible (pour filtrer)
                if mot in cws.lemma_names():
                    # On ajoute chacun des mots dans la bonne case de thématiques
                    for w in cws.lemma_names():
                        thematiques[count].append(w)
        else:
            # Nouvelle thématique
            newThematique = []
            for cws in closeWords:
                # On regarde si la liste du mot proche contient le mot cible (pour filtrer)
                if mot in cws.lemma_names():
                    # On ajoute chaque mot dans la nouvelle thématique
                    for w in cws.lemma_names():
                        newThematique.append(w)
            # Mot inconnu
            if len(newThematique) == 0:
                newThematique.append(mot)
            # Nouvelle thématique prête, on l'ajoute dans la liste
            thematiques.append(newThematique)
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))
    print(len(thematiques))
    print(len(df[col]))
    return thematiques

def extractThematique(thematiques):
    for i in range(0,len(thematiques)):
        # On récupère la thématique en dataframe
        df = DataFrame(thematiques[i], columns=["words"])
        # On rajoute un compteur sur chaque mot
        df["count"] = 1
        # On réduit les mots identiques
        grouped_df = df.groupby(["words"]).count()
        # On place en premier le mot représentant la thématique
        grouped_df = grouped_df.sort_values(by=["count"], ascending=False)
        # On refait une liste contenant les mots, sans doublon
        newList = df.iloc[:, 0].drop_duplicates().tolist()
        # Le mot ressortant le plus est la thématique
        keyTheme = newList[0]
        # On met à jour la thématique dans la liste
        thematiques[i] = (keyTheme,newList)
    return thematiques

if __name__ == '__main__':
    df1 = pandas.read_csv("data/map_reduced_subject.csv", low_memory=False, header=0)
    df1 = df1.dropna()
    df2 = pandas.read_csv("data/map_reduced_content.csv", low_memory=False, header=0)
    df2 = df2.dropna()

    thematiques1 = create_thematiques("Subject",df1)
    thematiques1 = extractThematique(thematiques1)

    #thematiques2 = create_thematiques("content",df2)
    #thematiques2 = extractThematique(thematiques2)

    for theme in thematiques1:
        print(theme)