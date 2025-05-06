import subprocess
from table_generation import *

sqlite_path = "/home/test/sqlite/sqlite3"
db_path = "test.db"

sql_cmd = generate_sqlite_table()

# Run the command
result = subprocess.run(
    [sqlite_path, db_path],
    input=sql_cmd,
    capture_output=True,
    text=True
)

print("STDOUT:\n", result.stdout)
print("STDERR:\n", result.stderr)
