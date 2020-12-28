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
        itemsets.append(thematiques)
    # On récupère le fp-tree
    start_time = time.time()
    patterns = pyfpgrowth.find_frequent_patterns(itemsets, 100)
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))

    # Et les règles d'association
    start_time = time.time()
    rules = pyfpgrowth.generate_association_rules(patterns, 0.8)
    stop_time = time.time()
    print("\nTemps de calcul = %f secondes" % (stop_time - start_time))

    # On retire les patterns seuls
    patternToPop = []
    for pattern in patterns:
        if(len(pattern) == 1):
            patternToPop.append(pattern)
    for pattern in patternToPop:
        patterns.pop(pattern)

    print(patterns)
    print(rules)

    # Nous allons mieux ranger les données
    patterns_df = pandas.DataFrame(columns=['pattern','count'])

    pattern_df = []
    count_df = []

    # On récupère les différents patterns et count
    for pattern in patterns:
        pattern_df.append(pattern)
        count_df.append(patterns.get(pattern))

    # On les ajoute dans le tableau
    patterns_df['pattern'] = pattern_df
    patterns_df['count'] = count_df
    patterns_df.sort_values(by=['count'])
    patterns_df.to_csv("data/itemsetsFrequents.csv")

    # Nous allons calculer le lift de ces règles
    rules_df = pandas.DataFrame(columns=['A','B','confiance','support','lift'])

    # Règle : pattern A --> pattern B
    A_df = []
    B_df = []
    conf_df = []
    support_df = []

    # On récupère les différentes associations
    for pattern in rules:
        A_df.append(pattern)
        B_df.append(rules.get(pattern)[0])
        conf_df.append(rules.get(pattern)[1])
        support_df.append(patterns.get(pattern))

    # On les ajoute dans le tableau
    rules_df['A'] = A_df
    rules_df['B'] = B_df
    rules_df['confiance'] = conf_df
    rules_df['support'] = support_df
    rules_df['lift'] = rules_df["confiance"] / rules_df["support"]
    rules_df.sort_values(by=['lift'])

    rules_df.to_csv("data/reglesEtCalculs.csv")