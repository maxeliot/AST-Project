import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "/workspace/results/expression_depth_counts.csv"
data = pd.read_csv(file_path)

# Calculate the percentage of queries for each depth
total_queries = data['Query Count'].sum()
data['Percentage'] = (data['Query Count'] / total_queries) * 100

# Plot the histogram with percentages
plt.bar(data['Expression Depth'], data['Percentage'], color='skyblue', edgecolor='black')
plt.xlabel('Expression Depth')
plt.ylabel('Percentage of Queries (%)')
plt.title('Histogram of Expression Depth vs Percentage of Queries')
plt.xticks(data['Expression Depth'])  # Ensure all depths are labeled
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot as an image
plt.savefig("/workspace/plots/expression_depth.png")
