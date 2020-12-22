from pyfpgrowth import *
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

if __name__ == '__main__':
    df1 = pandas.read_csv("data/mails_thematiques.csv", low_memory=False, header=0)
    itemsets = []
    # Pour chaque mail, on récupère ses thématiques
    for mailTraite in df1['Thematiques']:
        thematiques = retrieve_thematiques(mailTraite)
        # On met toutes les thématiques dans un tableau
        itemsets.append(thematiques)
    # On récupère le fp-tree
    patterns = pyfpgrowth.find_frequent_patterns(itemsets, 2)
    print(patterns)
    # Et les règles d'association
    rules = pyfpgrowth.generate_association_rules(patterns, 0.1)
    print(rules)
