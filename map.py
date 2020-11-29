import pandas as pandas

#Permet de split et d'avoir une ligne par string
def split_row(df,col):
    #Split chaque String de chaque ligne
    #Va créer un tableau de Strings
    df[col] = df.Subject.str.split(" ")
    print(df.head())
    #On va l'exploser, donc ajouter pour chaque string dans
    #les listes une nouvelle ligne avec juste le string
    df = df.explode(col)
    print(df.head())
    df["count"] = 1
    print(df.head())
    grouped_df = df.groupby([col]).count()
    grouped_df = grouped_df.sort_values(by=["count"], ascending=False)
    grouped_df.to_csv("data/map_reduced_subject.csv")
    print(grouped_df)

if __name__ == '__main__':
    df = pandas.read_csv("data/formatted_data.csv", low_memory=False, header=0)
    df = df[['Subject']].dropna()
    print(df.head())
    split_row(df,'Subject')