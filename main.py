from pandas import *

def formate_datas(csv_file):
    df = pandas.read_csv(csv_file, low_memory=False, header=0)

    df = df[['Message-ID', 'From', 'To', 'Subject', 'Content']]

    unwanted_ids = []
    for index, row in df.iterrows():
        if not(row['Message-ID'].startswith('<')):
            unwanted_ids.append(index)
        elif isinstance(row['content'], float):
                if isinstance(row['Subject'], float):
                    unwanted_ids.append(index)
        elif row['content'].startswith('---------------------- Forwarded by'):
            unwanted_ids.append(index)

    new_df = df.drop(unwanted_ids)
    return (new_df)

if __name__ == '__main__':
    df = formate_datas("data/donnees_data_science.csv")
    df.to_csv("data/formatted_data.csv")