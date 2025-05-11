import csv

import matplotlib.pyplot as plt

# File path to the CSV file
csv_file = '/workspace/results/coverage.csv'

# Initialize lists to store data
iterations = []
coverage = []

# Read data from the CSV file
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        iterations.append(int(row[0]))  # Assuming the first column is iterations
        coverage.append(float(row[1]))  # Assuming the second column is coverage

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(iterations, coverage, marker='o', linestyle='-', color='b', label='Coverage')

# Add labels, title, and legend
plt.xlabel('Number of Iterations')
plt.ylabel('Coverage')
plt.title('Coverage Over Iterations')
plt.legend()
plt.grid(True)

# Show the plot
plt.savefig("/workspace/plots/coverage_plot.png")