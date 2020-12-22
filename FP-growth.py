import time
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
    df1 = pandas.read_csv("data/mails_thematiquesV2.csv", low_memory=False, header=0)
    itemsets = []
    # Pour chaque mail, on récupère ses thématiques
    for mailTraite in df1['Thematiques']:
        thematiques = retrieve_thematiques(mailTraite)
        # On met toutes les thématiques dans un tableau
        print(thematiques)
        itemsets.append(thematiques)
    # On récupère le fp-tree
    start_time = time.time()
    patterns = pyfpgrowth.find_frequent_patterns(itemsets, 1)
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))
    print(patterns)
    # Et les règles d'association
    start_time = time.time()
    rules = pyfpgrowth.generate_association_rules(patterns, 0)
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))
    print(rules)
