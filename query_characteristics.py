import re
import csv
import sqlite_utils as sqlu

CLAUSES = ["SELECT", "JOIN", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "INSERT", "UPDATE", "DELETE",
               "CREATE TABLE", "DROP TABLE", "ALTER TABLE", "INDEX", "VIEW", "NOT"]

def analyze_query(query):
    """
    Analyze the SQL query for frequency of clauses, expression depth, and validity.

    Args:
        query (str): The SQL query to analyze.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    # Frequency of SQL clauses
    clauses = CLAUSES
    clause_counts = {clause: len(re.findall(rf"\b{clause}\b", query, re.IGNORECASE)) for clause in clauses}

    # Expression depth (count nested parentheses)
    expression_depth = 0
    max_depth = 0
    for char in query:
        if char == "(":
            expression_depth += 1
            max_depth = max(max_depth, expression_depth)
        elif char == ")":
            expression_depth -= 1

    # Return analysis results
    return {
        "clause_counts": clause_counts,
        "expression_depth": max_depth
    }

def is_query_valid(query, sqlite_version):
    """
    Check if the SQL query is valid by executing it.

    Args:
        query (str): The SQL query to execute.
        sqlite_version (str): The SQLite version to use.

    Returns:
        bool: True if the query is valid, False otherwise.
    """
    return sqlu.run_sqlite_query(query, sqlite_version)[1] == ""

def collect_statistics(schema):
    """
    Analyze SQL queries from a file and collect statistics.

    Args:
        schema (dict): The database schema (not used in this version).
        num_queries (int): The number of queries to analyze.
    """
    valid_queries = 0
    invalid_queries = 0
    total_clause_counts = {clause: 0 for clause in CLAUSES}

    # Read queries from the file
    queries_file = "/workspace/results/queries.txt"
    with open(queries_file, "r") as file:
        queries = [line.strip() for line in file if line.strip()]

    for query in queries:
        analysis = analyze_query(query)

        # Check query validity
        if is_query_valid(query, sqlu.SQLITE_3_26_0):
            valid_queries += 1
        else:
            invalid_queries += 1

        # Sum up clause counts
        for clause, count in analysis["clause_counts"].items():
            total_clause_counts[clause] += count

    # Output clause counts to a CSV file
    csv_file = "/workspace/results/clause_counts.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Clause", "Count"])
        for clause, count in total_clause_counts.items():
            writer.writerow([clause, count])

    # Print validity ratio
    print(f"Valid Queries: {valid_queries}, Invalid Queries: {invalid_queries}")
    print(f"Validity Ratio: {valid_queries / (valid_queries + invalid_queries):.2f}")


    # Log the validity ratio
    with open("/workspace/results/validity_ratio.txt", mode="w") as file:
        file.write(f"Validity Ratio: {valid_queries / (valid_queries + invalid_queries):.2f}\n")
        

# Example usage
if __name__ == "__main__":
    schema = {
        "t0": ["c0", "c1"],
        "t1": ["c0"]
    }
    collect_statistics(schema)