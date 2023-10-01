# Extremely work in progress

import csv
import matplotlib.pyplot as plt

points = [] # An array of converted points

# Change the name to match your file
with open('filtered-with-mnc.csv',newline='') as csvfile:
    data = csv.reader(csvfile,delimiter=';')

    for row in data:    
        # Row contains an array of words in the row
        # For me the structure is ['radio', 'area', 'cellid', 'signal', 'time', 'mnc']
        # Checking that if this is not the first line containing the information
        if 'area' not in row:
            point = {
                'time': row[4], # Do we want change this?
                'radio': row[0],
                'mnc': row[5],
                'signal': row[3]
            }
            points.append(point)
    
    csvfile.close()

#print(len(points)) # To see if gives 397 -> it does

xValues = [point['time'] for point in points]
yValues = [point['signal'] for point in points]
#print(yValues)

#xValues = [1,2,3,4,5]
#yValues = [-130, -95, -100, -110, -98]

plt.plot(xValues, yValues)
plt.xlabel('Unix timestamp time')
plt.ylabel('Signal value in dBm')
plt.savefig('data.png')