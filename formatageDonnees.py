import re
from pandas import *

def formate_datas(csv_file):
    df = pandas.read_csv(csv_file, low_memory=False, header=0)

    df = df[['Message-ID', 'From', 'To', 'Subject', 'content']]

    unwanted_ids = []
    for index, row in df.iterrows():
        #pour formatter les 'From' pour n'avoir que le nom de l'expéditeur
        row['From'] = re.search(r"frozenset\(\{('|\")(.*)@", row['From']).group(2)

        # pour formatter les 'To' pour n'avoir que le nom du destinataire
        #row['To'] = re.search(r"frozenset\(\{('|\")(.*)@", row['To']).group(2)

        #pour enlever les mails qui ne sont pas au bon format
        if not(row['Message-ID'].startswith('<')):
            unwanted_ids.append(index)
        elif isinstance(row['content'], float):
                if isinstance(row['Subject'], float):
                    unwanted_ids.append(index)

    new_df = df.drop(unwanted_ids)
    return (new_df)

if __name__ == '__main__':
    df = formate_datas("visualisation/data/donnees_data_science.csv")
    df.to_csv("visualisation/data/formatted_data.csv")