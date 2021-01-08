from pandas import *
import time

## IDMAIL + les thématiques dans un tableau ##

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
    df = pandas.read_csv("../data2/formatted_data.csv", low_memory=False, header=0)
    df = df[['From', 'Subject']].dropna()
    df1 = pandas.read_csv("../data/clean_thematiques.csv", low_memory=False, header=0)
    # les mails avec leurs thématiques
    mailsThematiques = []
    nbMail = 0
    # Pour chaque mail
    for mailTraite in df.iterrows():
        nbMail += 1
        print(nbMail)
        mailTraite[1].str.lower()
        # On crée une nouvelle ligne
        newMailRow = []
        # On indique quel mail on traite, on récupère son id
        idMail = mailTraite[0]
        From = mailTraite[1].From
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
                newMailRow.append(thematique)
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
                        newMailRow.append(thematique)
                    count += 1
        # Puis on ajoute notre mail avec ses thématiques dans le tableau (seulement s'il en a)
        if newMailRow:
            mailsThematiques.append((idMail,From,newMailRow))

    # On a fini d'attribuer les différentes thématiques aux mails
    mailsThematiques = pandas.DataFrame(mailsThematiques, columns = ["idEmail","From","Thematiques"])
    mailsThematiques.to_csv("../data2/mails_thematiquesV2.csv")
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))
    print("Nous avons %d mails comportant des thématiques sur %d mails au départ" % (len(mailsThematiques),len(df)))


if __name__ == '__main__':
    associate_to_mails()