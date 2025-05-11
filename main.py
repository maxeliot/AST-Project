import time
import query_generation
import sqlite_utils as sqlu
import subprocess
import table_generation
import glob
import os

import re
import csv

def coverage(iteration):
    """
    Run gcov, extract the coverage percentage, and append it to a CSV file.

    Args:
        iteration (int): The current iteration number.
    """
    # Run gcov and capture the output
    result = subprocess.run(
        f"gcov -r /home/test/sqlite/sqlite3-sqlite3.gcda",
        shell=True,
        capture_output=True,
        text=True
    )

    # Extract the coverage percentage using regex
    match = re.search(r"Lines executed:(\d+\.\d+)%", result.stdout)
    if match:
        coverage_percentage = float(match.group(1))  # Extract the percentage as a float
    else:
        coverage_percentage = 0.0  # Default to 0 if no match is found

    # Append the iteration and coverage to a CSV file
    csv_file = "/workspace/results/coverage.csv"
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([iteration, coverage_percentage])

def cleanup_gcda_files():
    """
    Remove all .gcda files to prevent gcov profiling errors.
    """
    for gcda_file in glob.glob("/home/test/sqlite/*.gcda"):
        os.remove(gcda_file)
        
    
if __name__ == "__main__":
    # Cleanup .gcda files before running the query
    cleanup_gcda_files()

    # Example schema
    schema = {
        "t0": ["c0", "c1"],
        "t1": ["c0"]
    }

    start_time = time.time()

    for i in range(100):
        query = query_generation.generateQuery(schema)
        #print("Generated Query: \n", query, "\n", sep="")

        result = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_26_0)

        rows_returned = result[0].split("\n")
        #print("Rows Returned on version 3.26.0:")
        #for row in rows_returned:
        #    print(row)
        #print()

        result = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_49_2)

        rows_returned2 = result[0].split("\n")
        #print("Rows Returned on version 3.49.2:")
        #for row in rows_returned2:
        #    print(row)
        #print()

        #print(f"Results on different versions match (order independent): {set(rows_returned2) == set(rows_returned)}")
        print(set(rows_returned2) == set(rows_returned))

        if(i % 10 == 0):
            coverage(i)



    print(f"Time taken to run the query: {time.time() - start_time} seconds")

    subprocess.run(["/workspace/measuring/coverage.sh"])
