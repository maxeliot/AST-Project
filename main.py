import time
import query_generation
import sqlite_utils as sqlu
import subprocess
import table_generation
import glob
import os
import argparse

import re
import csv

NUMBER_OF_QUERIES = 200
COVERAGE_INTERVAL = NUMBER_OF_QUERIES // 10 if NUMBER_OF_QUERIES > 10 else 1

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


def measure_performance_generation(number_queries):
    start_time = time.time()


    for i in range(number_queries):
        schema, tables_rows, sql_stmts, tables_stmts = table_generation.generate_tables()
        query_generation.generateQuery(schema)

    end_time = time.time()

    queries_per_minute = int((number_queries / (end_time - start_time)) * 60)

    # Output the performance metrics to a CSV file
    csv_file = "/workspace/results/perf-generation-only.csv"
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([queries_per_minute])

def measure_performance_all(number_queries):
    start_time = time.time()

    for i in range(number_queries):
        schema, tables_rows, sql_stmts, tables_stmts = table_generation.generate_tables()
        sql_query = table_generation.generate_sql_tables_query(sql_stmts, tables_stmts)
        result = sqlu.run_sqlite_query(sql_query, sqlu.SQLITE_3_26_0)

        query = query_generation.generateQuery(schema)

        result = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_26_0)
        rows_returned = result[0].split("\n")

        result2 = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_49_2)
        rows_returned2 = result2[0].split("\n")

        set(rows_returned2) != set(rows_returned)

    end_time = time.time()

    queries_per_minute = int((number_queries / (end_time - start_time)) * 60)

    # Output the performance metrics to a CSV file
    csv_file = "/workspace/results/perf-generation-execution.csv"
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([queries_per_minute])


        
    
if __name__ == "__main__":
    for i in range(10):
        measure_performance_generation(NUMBER_OF_QUERIES)
        measure_performance_all(NUMBER_OF_QUERIES)

    parser = argparse.ArgumentParser(description="Run performance and coverage tests.")
    parser.add_argument(
        "--num-queries",
        type=int,
        default=200,
        help="Number of queries to generate and test (default: 200)"
    )
    args = parser.parse_args()
    num_queries = args.num_queries
    coverage_interval = num_queries // 10 if num_queries > 10 else 1
    
    


    # Cleanup .gcda files before running the query
    cleanup_gcda_files()

    found_bug = False
    

    for i in range(num_queries):
        schema, tables_rows, sql_stmts, tables_stmts = table_generation.generate_tables()
        sql_query = table_generation.generate_sql_tables_query(sql_stmts, tables_stmts)

        result = sqlu.run_sqlite_query(sql_query, sqlu.SQLITE_3_26_0)

        query = query_generation.generateQuery(schema)

        # Log the generated query to a file
        cleaned_sql_query = sql_query.replace("\n", "")
        with open("/workspace/results/queries.txt", "a") as f:
            f.write(f"{cleaned_sql_query}{query}\n")

        result = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_26_0)
        rows_returned = result[0].split("\n")

        result2 = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_49_2)
        rows_returned2 = result2[0].split("\n")

        if set(rows_returned2) != set(rows_returned):
            found_bug = True
            print(f"Results on different versions do not match (order independent): {set(rows_returned2) != set(rows_returned)}")
            print("Rows returned on version 3.26.0:")
            for row in rows_returned:
                print(row)
            print()
            print("Rows returned on version 3.49.2:")
            for row in rows_returned2:
                print(row)
            print()


        if(i % coverage_interval == 0):
            coverage(i)
    
    if not found_bug:
        print("No bugs found in the generated queries.")
