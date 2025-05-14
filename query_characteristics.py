import re
import csv
import query_generation
import sqlite_utils as sqlu
#from sqlparse import parse  # Install sqlparse: pip install sqlparse

NUMBER_OF_QUERIES = 10

def analyze_query(query):
    """
    Analyze the SQL query for frequency of clauses, expression depth, and validity.

    Args:
        query (str): The SQL query to analyze.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    # Frequency of SQL clauses
    clauses = ["SELECT", "JOIN", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "INSERT", "UPDATE", "DELETE",
              "CREATE TABLE", "DROP TABLE", "ALTER TABLE", "INDEX", "VIEW"]
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
    #TODO this is not the right way to check for query validity
    try:
        sqlu.run_sqlite_query(query, sqlite_version)
        return True
    except Exception:
        return False

def collect_statistics(schema, num_queries):
    """
    Generate SQL queries, analyze them, and collect statistics.

    Args:
        schema (dict): The database schema.
        num_queries (int): The number of queries to generate.
    """
    valid_queries = 0
    invalid_queries = 0
    statistics = []

    for i in range(num_queries):
        query = query_generation.generateQuery(schema)
        analysis = analyze_query(query)

        # Check query validity
        if is_query_valid(query, sqlu.SQLITE_3_26_0):
            valid_queries += 1
        else:
            invalid_queries += 1

        # Collect statistics
        statistics.append({
            "query": query,
            "clause_counts": analysis["clause_counts"],
            "expression_depth": analysis["expression_depth"],
            "valid": is_query_valid(query, sqlu.SQLITE_3_26_0)
        })

    # Output statistics to a CSV file
    csv_file = "/workspace/results/query_statistics.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Query", "SELECT", "JOIN", "WHERE", "GROUP BY", "Expression Depth", "Valid"])
        for stat in statistics:
            writer.writerow([
                stat["query"],
                stat["clause_counts"]["SELECT"],
                stat["clause_counts"]["JOIN"],
                stat["clause_counts"]["WHERE"],
                stat["clause_counts"]["GROUP BY"],
                stat["expression_depth"],
                stat["valid"]
            ])

    # Print validity ratio
    print(f"Valid Queries: {valid_queries}, Invalid Queries: {invalid_queries}")
    print(f"Validity Ratio: {valid_queries / (valid_queries + invalid_queries):.2f}")

# Example usage
if __name__ == "__main__":
    schema = {
        "t0": ["c0", "c1"],
        "t1": ["c0"]
    }
    collect_statistics(schema, NUMBER_OF_QUERIES)