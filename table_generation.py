import random
import string
import sqlite_utils as sqlu

def generate_sqlite_table():
    """
    Generate a SQLite CREATE TABLE statement for a table named 't0'
    with 1-5 columns of random types.
    
    Returns:
        str: A valid SQLite CREATE TABLE statement
    """
    
    # Generate random number of columns (between 1 and 5)
    num_columns = random.randint(1, 5)
    
    # Generate column definitions
    columns = []
 
    
    for i in range(num_columns):
        
        column_name = f"c{i}"
        
        # Select a random data type
        data_type = random.choice(sqlu.DATA_TYPES)
        
        # Randomly decide if the column should have constraints
        constraints = []
        
        # 30% chance to add NOT NULL constraint
        if random.random() < 0.3:
            constraints.append("NOT NULL")
        
        # 20% chance to add PRIMARY KEY constraint (only if no primary key exists yet)
        # and ensuring at most one primary key per table
        if "PRIMARY KEY" not in str(columns) and random.random() < 0.2:
            constraints.append("PRIMARY KEY")
            
        # 10% chance to add UNIQUE constraint
        if random.random() < 0.1:
            constraints.append("UNIQUE")
            
        # 15% chance to add DEFAULT value (appropriate for the data type)
        if random.random() < 0.15:
            if data_type == "INTEGER":
                constraints.append(f"DEFAULT {random.randint(-100, 100)}")
            elif data_type == "REAL":
                constraints.append(f"DEFAULT {round(random.uniform(-100, 100), 2)}")
            elif data_type == "TEXT":
                constraints.append(f"DEFAULT 'default_{column_name}'")
            elif data_type == "NUMERIC":
                constraints.append(f"DEFAULT {random.randint(0, 100)}")
                
        # Combine column definition
        column_def = f"{column_name} {data_type}" + (f" {' '.join(constraints)}" if constraints else "")
        columns.append(column_def)
    
    # Create the complete SQL statement
    sql_statement = (
        "DROP TABLE IF EXISTS t0;"
        f"CREATE TABLE t0 (\n    " + ",\n    ".join(columns) + "\n);"
    )
    
    return sql_statement

# Example usage
if __name__ == "__main__":
    print(generate_sqlite_table())