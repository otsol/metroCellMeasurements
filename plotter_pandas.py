import datetime
import os

# import typing
import pandas as pd
import matplotlib.pyplot as plt
import pandas.errors

# class OperatorDataSet:
#     def __init__(self, operator: str, folder_name):
#         self.operator = operator
#         df = pd.DataFrame()

csv_output_folder = './csv_out/'
graph_output_folder = './graph_out/'

folders = ['./Otso-Kivenlahti', './Atif-Kivenlahti', './Juho-Kivenlahti', './Otso-Vuosaari', './Atif-Vuosaari',
           './Juho-Vuosaari']
operators = ['DNA', 'Elisa', 'Telia', 'DNA', 'Elisa', 'Telia']
terminals = {'Xiaomi_M2007J3SY': 'Xiaomi Mi 10T 5G', 'Xiaomi_23021RAAEG': 'Xiaomi Redmi Note 12',
             'Samsung_SM-S911B': 'Samsung Galaxy S23'}

for index, folder in enumerate(folders):
    tables = []
    for root, dirs, files in os.walk(os.path.abspath(folder)):
        for file in files:
            tables.append(os.path.join(root, file))

    print(len(tables))
    print()

    # Create an empty DataFrame to save csv contents
    df = pd.DataFrame()
    # Only read non-empty files and add them to the DataFrame
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
    df = df.sort_values(by=['time'], axis=0)

    # Finding the device
    terminal = df.iloc[1]['device']
    device = terminals.get(terminal)

    # Create a boolean column to show where cell ID changes
    df['cell_change'] = df['cellid'] != df['cellid'].shift()
    # Create a column for displaying time in formatted way
    df['formatted_time'] = df['time'].apply(
        lambda x: datetime.datetime.fromtimestamp(round(x / 1000)))
    df['min_from_start'] = df['formatted_time'].apply(
        lambda x: (x - df['formatted_time'].iloc[0]).total_seconds() / 60)

    # Save the DataFrame to CSV file
    df.to_csv(csv_output_folder + operators[index] + str(index) + '.csv', sep=';')

    # Plot and save the graph
    colors_indict = {'DNA': '#ff1493', 'Elisa': '#0000ff', 'Telia': '#800080'}
    df.plot(kind='line', x='min_from_start', y='signal', figsize=(20, 5), color=[colors_indict.get(operators[index])], label=operators[index])
    # df.plot(kind='line', x='time', y='signal')
    plt.title('Operator: ' + operators[index] + ', Device: ' + device)
    plt.xlabel('Minutes from start')
    plt.ylabel('Signal value in dBm')
    for idx, row in df.iterrows():
        if row['cell_change']:
            plt.axvline(x=row['min_from_start'], color='r', linestyle='--', linewidth='0.3', label='handoff point')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    #plt.legend([operators[index]],  loc='upper right')
    plt.savefig(graph_output_folder + operators[index] + str(index))
    plt.show()
