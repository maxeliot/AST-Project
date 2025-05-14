import re
import csv
import sqlite_utils as sqlu

CLAUSES = ["SELECT", "JOIN", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "INSERT", "UPDATE", "DELETE",
               "CREATE TABLE", "DROP TABLE", "ALTER TABLE", "INDEX", "VIEW", "NOT", "ABS", "LENGTH", "LOWER", "UPPER", "COALESCE",
               "CASE WHEN", "BETWEEN", "IN", "LIKE", "EXISTS", "UNION", "INTERSECT", "EXCEPT",]

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
    clause_counts = {clause: 1 if re.search(rf"\b{clause}\b", query, re.IGNORECASE) else 0 for clause in clauses}

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
    stdout, stderr =  sqlu.run_sqlite_query(query, sqlite_version)
    return stderr == ""

def collect_statistics():
    """
    Analyze SQL queries from a file and collect statistics.
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

    total_queries = valid_queries + invalid_queries

    # Output clause counts to a CSV file
    csv_file = "/workspace/results/clause_counts.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Clause", "Count"])
        writer.writerow(["Total Queries", total_queries])
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
    collect_statistics()