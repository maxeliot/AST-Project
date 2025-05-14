import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_path = "../results/clause_counts.csv"  # Adjust path if necessary
data = pd.read_csv(csv_path)

# Calculate percentages
total_queries = data.loc[data['Clause'] == 'Total Queries', 'Count'].values[0]
data['Percentage'] = (data['Count'] / total_queries) * 100

# Filter out 'Total Queries' row
data = data[data['Clause'] != 'Total Queries']

# Sort by descending frequency
data = data.sort_values(by='Count', ascending=False)

# Plot the histogram
plt.figure(figsize=(10, 8))
plt.barh(data['Clause'], data['Percentage'], color='skyblue')
plt.xlabel('Percentage (%)')
plt.ylabel('Clauses')
plt.title('Clause Frequency as Percentage of Total Queries')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest frequency at the top
plt.tight_layout()

# Save the plot
output_path = "../plots/clause_frequency_histogram.png"  # Adjust path if necessary
plt.savefig(output_path)
plt.show()