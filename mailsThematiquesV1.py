from pandas import *
import numpy as np
import time

## IDMAIL + des 0 et des 1 selon si le mail a ou non des thématiques ##

# Récupérer les mots associés à la thématique
def retrieve_associated_words(stringToChange):
    wordsAssociated = stringToChange
    wordsAssociated = wordsAssociated.replace("[", "")
    wordsAssociated = wordsAssociated.replace("]", "")
    wordsAssociated = wordsAssociated.replace(",", "")
    wordsAssociated = wordsAssociated.replace("'", "")
    wordsAssociated = wordsAssociated.split(" ")
    return wordsAssociated

# Selon son sujet
def associate_to_mails():
    start_time = time.time()
    df = pandas.read_csv("visualisation/data/formatted_data.csv", low_memory=False, header=0)
    df = df[['Subject']].dropna()
    df1 = pandas.read_csv("visualisation/data/clean_thematiques.csv", low_memory=False, header=0)
    columns = ["IDmail"]
    # Une ligne vide, qui va ensuite prendre les informations du mail
    emptyRow = [0]
    # On récupère les différentes thématiques
    for thematiques in df1["mainThematique"]:
        emptyRow.append(0)
        columns.append(thematiques)
    # les mails avec leurs thématiques
    mailsThematiques = pandas.DataFrame(columns=columns)
    nbMail = 0
    # Pour chaque mail
    for mailTraite in df.iterrows():
        nbMail += 1
        print(nbMail)
        mailTraite[1].str.lower()
        # On crée une nouvelle ligne
        newMailRow = emptyRow
        # On en fait un dataframe comprenant toutes les colonnes voulues
        newMailRow = pandas.DataFrame(data=np.array([newMailRow]), columns=columns)
        # On indique quel mail on traite, on récupère son id
        newMailRow["IDmail"] = mailTraite[0]
        # Pour chaque thématique existante
        for rowThemes in df1.iterrows():
            # La thématique que l'on traite
            thematique = rowThemes[1].mainThematique
            # Le sujet dans lequel on veut vérifier la thématique
            subject = mailTraite[1].Subject
            # Les mots associés à la thématique
            wordsAssociated = retrieve_associated_words(rowThemes[1].wordsAssociated)
            # On regarde si la thématique est présente
            if(thematique in subject):
                newMailRow[thematique] = 1
            # Sinon on regarde si un des mots proches est présents
            else:
                exist = False
                # On commence à 1 car le premier mot est la thématique
                count = 1
                while not exist and count < len(wordsAssociated):
                    # Le mot est présent ?
                    if (wordsAssociated[count] in subject):
                        # Oui, on indique que le mail est de cette thématique
                        exist = True
                        newMailRow[thematique] = 1
                    count += 1
        # Puis on ajoute notre mail avec ses thématiques dans le dataframe
        mailsThematiques = pandas.concat([mailsThematiques, newMailRow], ignore_index=True)
    # On a fini d'attribuer les différentes thématiques aux mails
    mailsThematiques.to_csv("data/mails_thematiquesV1.csv")
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))
    print("Nous avons %d mails comportant des thématiques sur %d mails au départ" % (len(mailsThematiques),len(df)))

if __name__ == '__main__':
    associate_to_mails()