import re
import numpy as np
from pandas import *

# Récupérer les thématiques associées à un mail
def retrieve_thematiques(stringToChange):
    wordsAssociated = stringToChange
    wordsAssociated = wordsAssociated.replace("[", "")
    wordsAssociated = wordsAssociated.replace("]", "")
    wordsAssociated = wordsAssociated.replace(",", "")
    wordsAssociated = wordsAssociated.replace("'", "")
    wordsAssociated = wordsAssociated.split(" ")
    return wordsAssociated

def extract_data(csv_file, them_file):
    them = pandas.read_csv(them_file, low_memory=False, header=0)
    df = pandas.read_csv(csv_file, low_memory=False, header=0)
    df = df[['From','Thematiques']]
    thematiques =[]
    for row in df['Thematiques']:
        thematiques.append(retrieve_thematiques(row))
    df['Thematiques']=thematiques
    new_df = df.groupby(['From'], sort=False)['Thematiques'].apply(lambda x : x.sum())
    list_dic = []
    for personne in new_df:
        compte = {k: personne.count(k) for k in set(personne)}
        list_dic.append(compte)
    print(list_dic)

    mails_df = df.groupby(['From'], sort=False).count()
    mails_df["Dictionnaire des thématiques"] = list_dic
    mails_df = mails_df.query('Thematiques>=50')
    mails_df = mails_df.rename(columns={"Thematiques": "Nombre d\'emails envoyés"})

    print(mails_df)

    return (mails_df)



if __name__ == '__main__':
    df = extract_data("../data2/mails_thematiquesV2.csv","../data/clean_thematiques.csv")
    #df.to_csv("../data2/FromExtracted.csv")