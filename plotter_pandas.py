import os

import pandas as pd
import matplotlib.pyplot as plt
import pandas.errors

dna_tables = []
for root, dirs, files in os.walk(os.path.abspath("./Otso")):
    for file in files:
        dna_tables.append(os.path.join(root, file))

print(len(dna_tables))
print()

# Create an empty DataFrame to save csv contents
df = pd.DataFrame()
# Only read non empty files and add them to the DataFrame
for file in dna_tables:
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

df.plot(kind='line', x='time', y='signal')
plt.xlabel('Unix timestamp time')
plt.ylabel('Signal value in dBm')
plt.savefig('data.png')
#df.plot(y='signal')

plt.show()
