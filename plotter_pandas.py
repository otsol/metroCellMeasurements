import os

# import typing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.errors


class OperatorDataSet:
    def __init__(self, operator: str, folder_name):
        self.operator = operator
        df = pd.DataFrame()


folders = ['./Otso', './Atif', './Juho']
operators = ['DNA', 'Elisa', 'Telia']


for index, folder in enumerate(folders):
    tables = []
    for root, dirs, files in os.walk(os.path.abspath(folder)):
        for file in files:
            tables.append(os.path.join(root, file))

    print(len(tables))
    print()

    # Create an empty DataFrame to save csv contents
    df = pd.DataFrame()
    # Only read non empty files and add them to the DataFrame
    for file in tables:
        try:
            raw_data = pd.read_table(file, delimiter=',')
            df = pd.concat([df, raw_data], axis=0)
        except pandas.errors.EmptyDataError:
            print(f"{file} is empty and has been skipped")

    # Save only unique rows
    df = df.drop_duplicates(subset='time')
    print('Size is:' + str(df.shape))
    print(df.columns)
    df = df.sort_values(by=['time'])

    # Create a boolean column to show where cell ID changes

    df['cell_change'] = df['cellid'] != df['cellid'].shift()
    df.to_csv(operators[index] + '.csv', sep=';')
    # Plot and save the graph
    df.plot(kind='line', x='time', y='signal', figsize=(20, 5))
    # df.plot(kind='line', x='time', y='signal')
    plt.xlabel('Unix timestamp time')
    plt.ylabel('Signal value in dBm')
    for idx, row in df.iterrows():
        if row['cell_change']:
            plt.axvline(x=row['time'], color='r', linestyle='--', linewidth='0.3')
    # df.plot(y='signal')
    plt.legend(operators[index])
    plt.savefig(operators[index])
    plt.show()
