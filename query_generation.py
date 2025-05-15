import random
import sqlite_utils as sqlu
import subprocess


MAX_DEPTH = 10

def generate_literal():
    kind = random.choice(["int", "text", "null"])
    if kind == "int":
        return str(random.randint(-1e6, 1e6))
    elif kind == "text":
        return f"'{random.choice(['foo', 'bar', 'baz'])}'"
    elif kind == "null":
        return "NULL"

def wrap_with_function(expr):
    functions = ["ABS", "LENGTH", "LOWER", "UPPER", "COALESCE"]
    func = random.choice(functions)
    if func == "COALESCE":
        alt = generate_literal()
        return f"{func}({expr}, {alt})"
    return f"{func}({expr})"

def generate_case_expression(depth, schema):
    cond = generateExpression(depth + 1, schema)
    then_expr = generateExpression(depth + 1, schema)
    else_expr = generateExpression(depth + 1, schema)
    return f"(CASE WHEN {cond} THEN {then_expr} ELSE {else_expr} END)"

def generate_special_binary(depth, schema):
    op = random.choice(["BETWEEN", "IN", "LIKE"])
    column = generateExpression(depth + 1, schema)
    if op == "BETWEEN":
        return f"{column} BETWEEN {generate_literal()} AND {generate_literal()}"
    elif op == "IN":
        in_list = ", ".join(generate_literal() for _ in range(random.randint(2, 5)))
        return f"{column} IN ({in_list})"
    elif op == "LIKE":
        pattern = f"'%{random.choice(['a', 'b', 'c'])}%'"
        return f"{column} LIKE {pattern}"

def generateExpression(depth, schema):
    """
    Generate a random SQL expression based on the given depth and schema.
    Args:
        depth (int): The current depth of the expression tree.
        schema (dict): A dictionary mapping a table to its columns.
    Returns:
        str: A randomly generated SQL expression.
    """ 
    if depth > MAX_DEPTH:
        return generate_literal()

    node_type = random.choices(
        ["LITERAL", "COLUMN", "UNARY", "BINARY", "CASE", "SPECIAL"],
        weights=[1, 1, 1, 2, 0.5, 0.5]
    )[0]

    if node_type == "LITERAL":
        return generate_literal()
    elif node_type == "COLUMN":
        table = random.choice(list(schema.keys()))
        column = random.choice(schema[table])
        expr = f"{table}.{column}"
        if random.random() < 0.3:
            expr = f"({expr} {random.choice(['IS NULL', 'IS NOT NULL'])})"
        elif random.random() < 0.5:
            expr = wrap_with_function(expr)
        return expr
    elif node_type == "UNARY":
        return f"NOT ({generateExpression(depth + 1, schema)})"
    elif node_type == "BINARY":
        op = random.choice(["=", "<", ">", "<=", ">=", "<>", "AND", "OR"])
        left = generateExpression(depth + 1, schema)
        right = generateExpression(depth + 1, schema)
        return f"({left} {op} {right})"
    elif node_type == "CASE":
        return generate_case_expression(depth, schema)
    elif node_type == "SPECIAL":
        return generate_special_binary(depth, schema)



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

    distinct = random.choice(["DISTINCT", ""])
    query = f"SELECT {distinct} {schema_columns} FROM {tables_join} WHERE {expression};"
    
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
    
