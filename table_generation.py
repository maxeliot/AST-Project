import random
import string
import sqlite_utils as sqlu
import query_generation as query

def generate_tables():

    """
    Generate multiple (between 1 and 3) CREATE TABLE statements with 1-5 columns and at least 1 row each.
    """

    # number of tables
    num_tables = random.randint(1, 3)

    tables = {} # Dictionary to store table names and their column names
    columns_tables = {}
    tables_rows = {} # Dictionary to store table names and their rows
    sql_stmts = {}
    primary_or_unique = {}
    tables_stmts = {}
    table_number = 0
    # Generate tables and add their column names to the dictionary
    for i in range(num_tables):
        stmt, columns, column_names = generate_sqlite_table(table_number)
        table_number += 1
        #print(stmt)
        tables_stmts["t" + str(i)] = stmt
        columns_tables["t" + str(i)] = columns
        tables["t" + str(i)] = column_names

    # TODO: add rows in better way, maybe store column types to help fill rows
    # Generate a random number of rows (between 1 and 5) for each table
    for table_name, column_names in tables.items():
        num_rows = random.randint(1, 5)
        rows = []
        sql_stmts[table_name] = ""  # Initialize the SQL statement for the table
        for i in range(num_rows):
            row_i, sql_stmt = generate_row(table_name, columns_tables[table_name], rows, tables)
            rows.append(row_i)
            sql_stmts[table_name] += sql_stmt
        tables_rows[table_name] = rows
        
    return tables, tables_rows, sql_stmts, tables_stmts

def generate_row(table_name, columns, rows, tables):
    # Generate a random row
    row_i = {}
    real_primary_key = []
    text_primary_key = []
    blob_primary_key = []
    primary_or_unique = False
    sql_stmts = ""
    for j, column_definition in enumerate(columns):
        # Generate a random value for each column
        
        column_constraints = column_definition.rsplit(' ')
        data_type = column_constraints[1]
        # if i == 0:
        #     print(f"Column {j}: {column_definition}")
        #     print(f"column type: {data_type}")
        if data_type == "NULL":
            row_i[j] = "NULL"
        # Check if the column has a NOT NULL constraint
        if "NOT" not in column_constraints:
            if random.random() < 0.1:
                row_i[j] = "NULL"
        if "PRIMARY" in column_constraints:
            # Generate a unique value for the primary key
            primary_or_unique = True
            if data_type == "INTEGER":
                row_i[j] = len(rows) + 1
            elif data_type == "REAL":
                real = round(random.uniform(-100, 100), 2)
                real_primary_key = [row[j] for row in rows if row.get(j) is not None]
                while real in real_primary_key:
                    real = round(random.uniform(-100, 100), 2)
                real_primary_key.append(real)
                row_i[j] = real
            elif data_type == "TEXT":
                text = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
                text_primary_key = [row[j] for row in rows if row.get(j) is not None]
                while text in text_primary_key:
                    text = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
                text_primary_key.append(text)
                row_i[j] = text
            elif data_type == "BLOB":
                blob = bytes(random.getrandbits(8) for _ in range(random.randint(1, 10)))
                blob_primary_key = [row[j] for row in rows if row.get(j) is not None]
                while blob in blob_primary_key:
                    blob = bytes(random.getrandbits(8) for _ in range(random.randint(1, 10)))
                blob_primary_key.append(blob)
                row_i[j] = blob
        elif "UNIQUE" in column_constraints and not row_i.get(j):
            primary_or_unique = True
            # Generate a unique value for the UNIQUE column
            if data_type == "INTEGER":

                row_i[j] = len(rows) + 1
            elif data_type == "REAL":
                real = round(random.uniform(-100, 100), 2)
                real_primary_key = [row[j] for row in rows if row.get(j) is not None]
                while real in real_primary_key:
                    real = round(random.uniform(-100, 100), 2)
                real_primary_key.append(real)
                row_i[j] = real
            elif data_type == "TEXT":
                text = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
                text_primary_key = [row[j] for row in rows if row.get(j) is not None]
                while text in text_primary_key:
                    text = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
                text_primary_key.append(text)
                row_i[j] = text
            elif data_type == "BLOB":
                blob = bytes(random.getrandbits(8) for _ in range(random.randint(1, 10)))
                blob_primary_key = [row[j] for row in rows if row.get(j) is not None]
                while blob in blob_primary_key:
                    blob = bytes(random.getrandbits(8) for _ in range(random.randint(1, 10)))
                blob_primary_key.append(blob)
                row_i[j] = blob
        # if "CHECK" in column_constraints:
        # for now only maybe sets default value if not unique
        # sets default value 25% of the time
        elif "DEFAULT" in column_constraints:
            if random.random() < 0.25:
                if "COLLATE" not in column_constraints:     #f" {' '.join(constraints)}"
                    default_index = column_constraints.index("DEFAULT") + 1
                    row_i[j] = " ".join(column_constraints[default_index:len(column_constraints)])
                else:
                    default_index = column_constraints.index("DEFAULT") + 1
                    row_i[j] = " ".join(column_constraints[default_index:len(column_constraints) - 2])
        if not row_i.get(j):
            if data_type == "INTEGER":
                row_i[j] = random.randint(-100, 100)
            elif data_type == "REAL":
                row_i[j] = round(random.uniform(-100, 100), 2)
            elif data_type == "TEXT":
                row_i[j] = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
            elif data_type == "BLOB":
                row_i[j] = bytes(random.getrandbits(8) for _ in range(random.randint(1, 10)))
    # Generate the SQL statement for inserting the row
    # if one column has unique or primary key constraint, 
    if len(rows) > 0 and primary_or_unique:
        # 20% chance to use INSERT OR REPLACE
        if random.random() < 0.2:
            sql_stmts += f"REPLACE INTO {table_name} ({', '.join(tables[table_name])}) VALUES ({', '.join([str(row_i[j]) for j in range(len(tables[table_name]))])});\n"
        # 20% chance to use INSERT OR IGNORE
        elif random.random() < 0.2:
            sql_stmts += f"INSERT OR IGNORE INTO {table_name} ({', '.join(tables[table_name])}) VALUES ({', '.join([str(row_i[j]) for j in range(len(tables[table_name]))])});\n"
        # 20% chance to use INSERT OR ROLLBACK
        elif random.random() < 0.2:
            sql_stmts += f"INSERT OR ROLLBACK INTO {table_name} ({', '.join(tables[table_name])}) VALUES ({', '.join([str(row_i[j]) for j in range(len(tables[table_name]))])});\n"
        # 20% chance to use INSERT OR ABORT
        elif random.random() < 0.2:
            sql_stmts += f"INSERT OR ABORT INTO {table_name} ({', '.join(tables[table_name])}) VALUES ({', '.join([str(row_i[j]) for j in range(len(tables[table_name]))])});\n"
        # 20% chance to use INSERT OR FAIL
        elif random.random() < 0.2:
            sql_stmts += f"INSERT OR FAIL INTO {table_name} ({', '.join(tables[table_name])}) VALUES ({', '.join([str(row_i[j]) for j in range(len(tables[table_name]))])});\n"
        else:
            sql_stmts += f"INSERT INTO {table_name} ({', '.join(tables[table_name])}) VALUES ({', '.join([str(row_i[j]) for j in range(len(tables[table_name]))])});\n"
    else:
        # 30% chance don't insert all columns
        if random.random() < 0.3:
            # Select a random number of columns to insert (between 1 and all columns)
            num_columns_to_insert = random.randint(1, len(tables[table_name]))
            # Select random column indices to insert
            column_indices = random.sample(range(len(tables[table_name])), num_columns_to_insert)
            # Create the SQL statement for inserting the row
            sql_stmts += f"INSERT INTO {table_name} ({', '.join([tables[table_name][j] for j in column_indices])}) VALUES ({', '.join([str(row_i[j]) for j in column_indices])});\n"
        # 30% chance for SELECT statement
        elif random.random() < 0.3:
            # TODO: add more complex SELECT statements
            selected_column = random.choice(tables[table_name])
            select_stmt = query.generateQuery(tables)
            sql_stmts += f"INSERT INTO {table_name} ({', '.join(tables[table_name])}) {select_stmt};\n"
            print(sql_stmts)
    return row_i, sql_stmts

def generate_sqlite_table(table_number):
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
    column_names = []
 
    
    for i in range(num_columns):
        
        column_name = f"c{i}"
        column_names.append(column_name)
        
        # Select a random data type
        data_type = random.choice(sqlu.DATA_TYPES)
        
        # Randomly decide if the column should have constraints
        constraints = []
        
        # 30% chance to add NOT NULL constraint
        if random.random() < 0.3 and data_type != "NULL":
            constraints.append("NOT NULL")
        
        # 20% chance to add PRIMARY KEY constraint (only if no primary key exists yet)
        # and ensuring at most one primary key per table
        if "PRIMARY KEY" not in str(columns) and random.random() < 0.2 and data_type != "NULL":
            constraints.append("PRIMARY KEY")
            
        # 20% chance to add UNIQUE constraint
        if random.random() < 0.2 and data_type != "NULL":
            constraints.append("UNIQUE")

        # # 20% chance to add CHECK constraint
        # if random.random() < 0.2:
        #     if data_type == "INTEGER":
        #         if random.random() < 0.3:
        #             constraints.append(f"CHECK({column_name} {random.choice(['>=', '<=', '==', '>', '<', '!='])} {random.randint(-50, 50)})")
        #         elif random.random() < 0.3:
        #             constraints.append(f"CHECK({column_name} BETWEEN {random.randint(-50, 0)} AND {random.randint(1, 50)})")
        #         # MAYBE TODO: add more complex check constraints
        #     elif data_type == "REAL":
        #         if random.random() < 0.5:
        #             constraints.append(f"CHECK({column_name} {random.choice(['>=', '<=', '==', '>', '<', '!='])} {random.uniform(-50, 50)})")
        #         else:
        #             constraints.append(f"CHECK({column_name} BETWEEN {random.uniform(-50, 0)} AND {random.uniform(1, 50)})")
        #         # MAYBE TODO: add more complex check constraints
        #     elif data_type == "TEXT":
        #         constraints.append(f"CHECK(length({column_name}) <= 50)")
        #     elif data_type == "BLOB":
        #         constraints.append(f"CHECK(length({column_name}) <= 100)")
        #     # elif data_type == "NUMERIC": -- sqlite does not have a NUMERIC type
        #     #     constraints.append(f"CHECK({column_name} >= 0)")
            
        # 20% chance to add DEFAULT value (appropriate for the data type)
        if random.random() < 0.2 and data_type != "NULL":
            if data_type == "INTEGER":
                constraints.append(f"DEFAULT {random.randint(-100, 100)}")
            elif data_type == "REAL":
                constraints.append(f"DEFAULT {round(random.uniform(-100, 100), 2)}")
            elif data_type == "TEXT":
                constraints.append(f"DEFAULT 'default_{column_name}'")
            elif data_type == "BLOB":
                constraints.append("DEFAULT x'00'")
            # elif data_type == "NUMERIC": -- sqlite does not have a NUMERIC type
            #     constraints.append(f"DEFAULT {random.randint(0, 100)}")

        # if data type is text, 30% chance to add collate function 
        if data_type == "TEXT":
            if random.random() < 0.3:
                collate_function = random.choice(["NOCASE", "RTRIM", "BINARY"])
                constraints.append(f"COLLATE {collate_function}")
                
        # Combine column definition
        column_def = f"{column_name} {data_type}" + (f" {' '.join(constraints)}" if constraints else "")
        columns.append(column_def)
    
    # Create the complete SQL statement
    sql_statement = "DROP TABLE IF EXISTS t" + f"{table_number}" + "; \n" f"CREATE TABLE t" + f"{table_number}" + " (\n    " + ",\n    ".join(columns) + "\n);"
    
    
    return sql_statement, columns, column_names

def select_pivot_row(tables_rows):
    """
    Select a random row from the given tables_rows dictionary.
    
    Args:
        tables_rows (dict): Dictionary containing table names and their rows.
        
    Returns:
        tuple: A tuple containing the table name and the selected row.
    """
    pivot_rows = {}
    for table_name, rows in tables_rows.items():
        # Select a random row from the table
        row = random.choice(rows)
        pivot_rows[table_name] = row
    return pivot_rows

def generate_sql_tables_query(tables, sql_stmts, tables_stmts):
    """
    Generate a SQL query to create the tables and insert the rows.
    
    Args:
        tables (dict): Dictionary containing table names and their columns.
        sql_stmts (dict): Dictionary containing table names and their SQL statements.
        
    Returns:
        str: A SQL query to create the tables and insert the rows.
    """
    sql_query = ""
    for stmt in tables_stmts.values():
        sql_query += stmt + "\n"
    for stmt in sql_stmts.values():
        sql_query += stmt + "\n"
    return sql_query

# Example usage
if __name__ == "__main__":
    # sql_stmt, columns, column_names = generate_sqlite_table()
    # print(sql_stmt)

    tables, tables_rows, sql_stmts, tables_stmts = generate_tables()
    print("Tables and their columns:")
    for table_name, column_names in tables.items():
        print(f"{table_name}: {column_names} \n")
    print("\nTables and their rows:")
    for table_name, rows in tables_rows.items():
        print(f"{table_name}: {rows} \n")
        print(sql_stmts[table_name] + "\n")

    pivot_rows = select_pivot_row(tables_rows)
    print("Pivot rows:")
    for table_name, row in pivot_rows.items():
        print(f"{table_name}: {row} \n")
    
    sql_query = generate_sql_tables_query(tables, sql_stmts, tables_stmts)
    print("SQL Query to create tables and insert rows:")
    print(sql_query)
