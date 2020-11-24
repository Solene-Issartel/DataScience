from pandas import *


def formate_datas(csv_file):
    df = pandas.read_csv(csv_file, low_memory=False, header=0)
    df = df[['From', 'To', 'Subject', 'X-cc', 'content']]

    unwanted_ids = []
    for index, row in df.iterrows():
        if isinstance(row['content'], float):
                if isinstance(row['content'], float) :
                    if isinstance(row['X-cc'], float):
                        unwanted_ids.append(index)
                    elif row['X-cc'].startswith('---------------------- Forwarded by'):
                        unwanted_ids.append(index)
        elif row['content'].startswith('---------------------- Forwarded by'):
            unwanted_ids.append(index)

    new_df = df.drop(unwanted_ids)
    return (new_df)


if __name__ == '__main__':
    df = formate_datas("data/donnees_data_science.csv")
    df.to_csv("data/formatted_data.csv")
