from pandas import *


if __name__ == '__main__':
    df = pandas.read_csv("data/donnees_data_science.csv", low_memory=False, header=0)
    df2 = df.head(30)
    df2 = df2[['From', 'To', 'Subject', 'X-cc', 'content']]

    unwanted_ids = []
    for index, row in df2.iterrows():
        if len(row['content']) == 0 \
                and len(row['Subject']) == 0 \
                and (len(row['X-cc']) or row['X-cc'].startswith('---------------------- Forwarded by')) == 0:
            unwanted_ids.append(index)
        elif row['content'].startswith('---------------------- Forwarded by'):
            unwanted_ids.append(index)

    print(unwanted_ids)
    new_df = df2.drop(unwanted_ids)
    print(new_df)
