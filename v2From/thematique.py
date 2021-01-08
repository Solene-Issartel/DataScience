from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from pandas import *
import time

## Un peu comme une méthode k-means permettant de regrouper les mots les plus proches ##
## selon leur similarité. On ne sait pas à l'avance quels mots vont se retrouver avec ##
## quels mots.                                                                        ##

def create_thematiques(col,df):
    start_time = time.time()
    # La liste qui contiendra les thématiques avec tous leurs mots associées
    thematiques = []
    # Les thématiques avec seulement les mots apparaissant de bases en mots associés
    realThematiques = []
    # Pour chaque mot récupéré dans les subjects
    for motBrut in df[col]:
        # On enlève les mots au pluriel
        mot = WordNetLemmatizer().lemmatize(motBrut)
        # On récupère les mots proches du mot actuel
        closeWords = wordnet.synsets(mot)
        exist = False
        count = 0
        # On regarde si on a déjà eu ce mot dans les mots proches précédents
        while (count < len(thematiques) and not exist):
            if (mot in thematiques[count]):
                exist = True
            else:
                # Tester la similarité du mot avec les thématiques déjà trouvées
                # seulement si le mot existe dans la librairie wordnet
                if (len(closeWords) != 0):
                    for motsTestés in thematiques[count]:
                        # On récupère les synonymes d'un des mots
                        synsetMT = wordnet.synsets(motsTestés)
                        # Seulement si le mot existe dans wordnet
                        if(len(synsetMT) != 0):
                            # On prend juste le premier
                            synsetMT = synsetMT[0]
                            similarity = (closeWords[0]).wup_similarity(synsetMT)
                            if(similarity == None):
                                similarity = 0
                            # On regarde s'ils sont similaires
                            if(similarity >= 0.65):
                                exist = True
            # On passe à la ligne suivante si on n'a pas trouvé de mot similaire
            if (not exist):
                count += 1
        if (exist):
            # Mot déjà traité, on le rajoute dans la bonne case
            for cws in closeWords:
                # On regarde si la liste du mot proche contient le mot cible (pour filtrer)
                if mot in cws.lemma_names():
                    # On ajoute chacun des mots dans la bonne case de thématiques
                    for w in cws.lemma_names():
                        thematiques[count].append(w)
                        if(w == mot):
                         realThematiques[count].append(motBrut)
        else:
            # Nouvelle thématique
            newRealThematique = []
            newThematique = []
            for cws in closeWords:
                # On regarde si la liste du mot proche contient le mot cible (pour filtrer)
                if mot in cws.lemma_names():
                    # On ajoute chaque mot dans la nouvelle thématique
                    for w in cws.lemma_names():
                        newThematique.append(w)
                        if(w == mot):
                            newRealThematique.append(motBrut)
            # Mot inconnu
            if len(newThematique) == 0:
                newThematique.append(mot)
                newRealThematique.append(motBrut)
            # Nouvelle thématique prête, on l'ajoute dans la liste
            thematiques.append(newThematique)
            realThematiques.append(newRealThematique)
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))
    print("Nous passons de %d à %d thématiques " % (len(df[col]), len(realThematiques)))
    return realThematiques

def extractThematique(thematiques):
    for i in range(0,len(thematiques)):
        # On récupère les thématiques en dataframe
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

    thematiques1 = create_thematiques("Subject",df1)
    thematiques1 = extractThematique(thematiques1)
    thematiques1 = pandas.DataFrame(thematiques1, columns=["mainThematique","wordsAssociated"])
    thematiques1.to_csv("data/clean_thematiques.csv")