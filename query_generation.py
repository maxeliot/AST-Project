import random
import sqlite_utils as sqlu
import subprocess


MAX_DEPTH = 3


def generateExpression(depth, schema):
    """
    Generate a random SQL expression based on the given depth and schema.
    Args:
        depth (int): The current depth of the expression tree.
        schema (dict): A dictionary mapping a table to its columns.
    Returns:
        str: A randomly generated SQL expression.
    """ 
    types = ["LITERAL", "COLUMN"]
    if depth < MAX_DEPTH:
        types.extend(["UNARY", "BINARY"])
    
    node_type = random.choice(types)
    if node_type == "LITERAL":
        return str(random.randint(-100, 100))
    elif node_type == "COLUMN":
        #table_column = random.choice(list(schema.keys()))
        table = random.choice(list(schema.keys()))
        column = random.choice(schema[table])
        table_column = f"{table}.{column}"
        return f"({table_column} {random.choice(['', ' IS NULL', ' IS NOT NULL'])})"
    elif node_type == "UNARY":
        operator = "NOT"
        expression = generateExpression(depth + 1, schema)
        return f"{operator} {expression}"
    elif node_type == "BINARY":
        operator = random.choice(["=", "<", ">", "<=", ">=", "<>", "AND", "OR"])
        left_expression = generateExpression(depth + 1, schema)
        right_expression = generateExpression(depth + 1, schema)
        return f"{left_expression} {operator} {right_expression}"


def generateQuery(schema):
    """
    Generate a random SQL query based on the given schema.
    Args:
        schema (dict): A dictionary mapping a table to its columns.
    Returns:
        str: A randomly generated SQL query.
    """

    # Generate a random expression
    expression = generateExpression(0, schema)
    
    # Create a SELECT statement
    tables = schema.keys()
    schema_columns = []
    for table in tables:
        columns = schema[table]
        for column in columns:
            schema_columns.append(f"{table}.{column}")
    schema_columns = ", ".join(schema_columns)
    
    tables_join = " CROSS JOIN ".join(tables)

    query = f"SELECT {schema_columns} FROM {tables_join} WHERE {expression};"
    
    return query


# Example usage
if __name__ == "__main__":

    schema = {
        "t0": ["c0", "c1"],
        "t1": ["c0"]
    }

    query = generateQuery(schema)
    print("Generated Query: \n", query, "\n", sep="")

    result = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_26_0)

    rows_returned = result[0].split("\n")
    print("Rows Returned on version 3.26.0:")
    for row in rows_returned:
        print(row)
    
    print()

    result = sqlu.run_sqlite_query(query, sqlu.SQLITE_3_49_2)

    rows_returned2 = result[0].split("\n")
    print("Rows Returned on version 3.49.2:")
    for row in rows_returned2:
        print(row)
    print()

    print(f"Results on different versions match (order independent): {set(rows_returned2) == set(rows_returned)}")
    
