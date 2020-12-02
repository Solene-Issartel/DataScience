import pandas as pandas

#Permet de split et d'avoir une ligne par string
def split_row(df,col,nameFile):
    #On met tout en majuscule
    df[col] = df[col].str.upper()
    #Split chaque String de chaque ligne, ce qui va créer des tableaux de string
    df[col] = df[col].str.split("\ |\:|\!|\?|\-|\"|\(|\)|\[|\]|\<|\>")
    #On va l'exploser, donc ajouter pour chaque string dans
    #les listes une nouvelle ligne avec juste un string
    df = df.explode(col)
    #On va mettre 1 pour chaque mot
    df["count"] = 1
    #On regroupe chaque mot, et on additionne leur count
    #On aura donc le nombre d'occurences de chaque mot
    grouped_df = df.groupby([col]).count()
    #On trie par ordre décroissant
    grouped_df = grouped_df.sort_values(by=["count"], ascending=False)
    grouped_df = grouped_df.query('count>10')
    grouped_df.to_csv(nameFile)
    print(grouped_df)
    #On regarde combien on a de catégories
    print(len(grouped_df))

if __name__ == '__main__':
    df = pandas.read_csv("data/formatted_data.csv", low_memory=False, header=0)
    df1 = df[['Subject']].dropna()
    print(df1)
    split_row(df1,'Subject',"data/map_reduced_subject.csv")
    df2 = df[['content']].dropna()
    print(df2)
    split_row(df2,'content',"data/map_reduced_content.csv")