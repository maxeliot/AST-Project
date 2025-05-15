# import csv
# import statistics

# def parse_csv_and_calculate_stats(file_path):
#     """
#     Parse a CSV file containing a single value per row and calculate the mean and standard deviation.

#     Args:
#         file_path (str): Path to the CSV file.

#     Returns:
#         tuple: Mean and standard deviation of the values in the file.
#     """
#     values = []

#     # Read the CSV file
#     with open(file_path, mode="r") as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row:  # Ensure the row is not empty
#                 values.append(int(row[0]))

#     # Calculate mean and standard deviation
#     mean = statistics.mean(values)
#     std_dev = statistics.stdev(values)

#     return mean, std_dev


# # File paths
# performance_generation_file = "/workspace/results/performance-generation.csv"
# performance_all_file = "/workspace/results/performance-all.csv"

# # Calculate stats for both files
# gen_mean, gen_std_dev = parse_csv_and_calculate_stats(performance_generation_file)
# all_mean, all_std_dev = parse_csv_and_calculate_stats(performance_all_file)

# # Output the results
# print(f"Performance Generation - Mean: {gen_mean}, Standard Deviation: {gen_std_dev}")
# print(f"Performance All - Mean: {all_mean}, Standard Deviation: {all_std_dev}")

import csv
import statistics

def parse_csv_and_calculate_stats(file_path):
    """
    Parse a CSV file containing a single value per row and calculate the mean and standard deviation.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        tuple: Mean and standard deviation of the values in the file.
    """
    values = []

    # Read the CSV file
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Ensure the row is not empty
                values.append(int(row[0]))

    # Calculate mean and standard deviation
    mean = statistics.mean(values)
    std_dev = statistics.stdev(values)

    return mean, std_dev


# File paths
performance_generation_file = "/workspace/results/perf-generation-only.csv"
performance_all_file = "/workspace/results/perf-generation-execution.csv"

# Calculate stats for both files
gen_mean, gen_std_dev = parse_csv_and_calculate_stats(performance_generation_file)
all_mean, all_std_dev = parse_csv_and_calculate_stats(performance_all_file)

# Output the results with thousands separators
print(f"Generated queries per minute - Mean: {gen_mean:,.0f}, Standard Deviation: {gen_std_dev:,.0f}")
print(f"Generated and executed queries per minute  - Mean: {all_mean:,.0f}, Standard Deviation: {all_std_dev:,.0f}")