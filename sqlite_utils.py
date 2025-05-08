import subprocess

DATA_TYPES = [
    "NULL",
    "INTEGER",
    "REAL",
    "TEXT",
    "BLOB"
]

SQLITE_PATH = "/home/test/sqlite/sqlite3"
DB_PATH = "test.db"

def run_sqlite_query(query):
    """
    Runs a given SQL query using the SQLite binary and captures its output.

    Args:
        query (str): The SQL query to execute.

    Returns:
        tuple: A tuple containing the standard output and standard error from the SQLite command.
    """
    result = subprocess.run(
        [SQLITE_PATH, DB_PATH],
        input=query,
        capture_output=True,
        text=True
    )
    return result.stdout.strip("\n"), result.stderr.strip("\n")


# Example usage
if __name__ == "__main__":
    query = "SELECT sqlite_version();"
    stdout, stderr = run_sqlite_query(query)
    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)