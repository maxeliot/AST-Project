import subprocess

DATA_TYPES = [
    "NULL",
    "INTEGER",
    "REAL",
    "TEXT",
    "BLOB"
]

SQLITE_3_26_0 = "/home/test/sqlite/sqlite3" # Use this path as it allows for coverage with gcov
SQLITE_3_39_4 = "/usr/bin/sqlite3-3.39.4"
SQLITE_3_49_2 = "/usr/bin/sqlite3-3.49.2"

DB_PATH = "test.db"




def run_sqlite_query(query, sqlite_path):
    """
    Runs a given SQL query using the SQLite binary and captures its output.

    Args:
        query (str): The SQL query to execute.

    Returns:
        tuple: A tuple containing the standard output and standard error from the SQLite command.
    """ 

    result = subprocess.run(
        [sqlite_path, DB_PATH],
        input=query,
        capture_output=True,
        text=True
    )
    return result.stdout.strip("\n"), result.stderr.strip("\n")


# Example usage
if __name__ == "__main__":
    query = "SELECT sqlite_version();"
    stdout, stderr = run_sqlite_query(query, SQLITE_3_26_0)
    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)