import subprocess

sqlite_path = "/home/test/sqlite/sqlite3"
db_path = ":memory:"

# Example SQL command
sql_cmd = 
"""
DROP TABLE IF EXISTS t0;
CREATE TABLE t0 ( c0 INT );
INSERT INTO t0 ( c0 ) VALUES (1);
SELECT * FROM t0 WHERE 1 = 1;
"""

# Run the command
result = subprocess.run(
    [sqlite_path, db_path],
    input=sql_cmd,
    capture_output=True,
    text=True
)

print("STDOUT:\n", result.stdout)
print("STDERR:\n", result.stderr)
