import pandas as pd
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the results directory
results_dir = os.path.join(current_dir, "../results")

# Load the CSV file
csv_path = os.path.join(results_dir, "clause_counts.csv")
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
output_path = os.path.join(current_dir, "clause_frequency_histogram.png")
plt.savefig(output_path)
plt.show()