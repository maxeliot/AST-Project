import time
import query_generation
import sqlite_utils as sqlu
import subprocess
import table_generation
import glob
import os

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

    for i in range(3_000):
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


    print(f"Time taken to run the query: {time.time() - start_time} seconds")

    subprocess.run(["/workspace/measuring/coverage.sh"])
