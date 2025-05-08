import random
import sqlite_utils as sqlu
import subprocess


MAX_DEPTH = 3


def generateExpression(depth, pivot_row):
    """
    Generate a random SQL expression based on the given depth and schema.
    Args:
        depth (int): The current depth of the expression tree.
        pivot_row (dict): A dictionary mapping "table.column" to its value.
    Returns:
        str: A randomly generated SQL expression.
    """ 
    types = ["LITERAL", "COLUMN"]
    if depth < MAX_DEPTH:
        types.append("UNARY")
    
    node_type = random.choice(types)
    if node_type == "LITERAL":
        return str(random.randint(-100, 100))
    elif node_type == "COLUMN":
        table_column = random.choice(list(pivot_row.keys()))
        return table_column
    elif node_type == "UNARY":
        # TODO FIGURE OUT HOW TO GENERATE A RANDOM OPERATOR WITH IS NULL WITHOUT BUGS
        #operator = random.choice(["NOT", "IS NULL", "IS NOT NULL"])
        operator = "NOT"
        expression = generateExpression(depth + 1, pivot_row)
        return f"{operator} {expression}"



def rewriteExpression(expression, pivot_row):
    """
    Rewrite an SQL-like expression by replacing column references with actual values from the pivot row.

    Args:
        expression (str): The SQL-like expression to evaluate.
        pivot_row (dict): A dictionary mapping "table.column" to its value.

    Returns:
        str: The rewritten expression with column references replaced by their values.
    """
    tokens = expression.split()
    evaluated_tokens = []

    for token in tokens:
        if token in pivot_row:  # Check if the token is a column reference
            value = pivot_row[token]
            # Add quotes for string values
            if isinstance(value, str):
                evaluated_tokens.append(f"'{value}'")
            else:
                evaluated_tokens.append(str(value))
        else:
            evaluated_tokens.append(token)

    return " ".join(evaluated_tokens)


def evaluateExpression(expression, pivot_row):
    """
    Evaluate an SQL-like expression by replacing column references with actual values from the pivot row.

    Args:
        expression (str): The SQL-like expression to evaluate.
        pivot_row (dict): A dictionary mapping "table.column" to its value.

    Returns:
        str: The evaluated expression with column references replaced by their values.
    """
    # Rewrite the expression using the pivot row
    rewritten_expression = "SELECT " + rewriteExpression(expression, pivot_row)
    
    return sqlu.run_sqlite_query(rewritten_expression)


def rectifyCondition(expression, pivot_row):
    output = evaluateExpression(expression, pivot_row)[0]
    if(output == "1"):
        return expression
    elif(output == "0"):
        return "NOT " + expression
    elif(output == "NULL"):
        return expression + " IS NULL"
    
    return expression


# Example usage
if __name__ == "__main__":

    pivot_row = {
        "t0.c0": 42,
        "t0.c1": "example",
        "t1.c0": "test",
    }
    
    
    expression = generateExpression(0, pivot_row)
    
    print("Pivot Row:", pivot_row)
    print("Generated Expression:", expression)
    print("Corrected Expression:", rectifyCondition(expression, pivot_row))





################################################################################
# MAYBE USEFUL FOR FUTURE
################################################################################

"""
class Literal:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def execute(self):
        return self.value

    def randomLiteral(self):
        lit_type = random.choice(sqlu.DATA_TYPES)
        if lit_type == "INTEGER":
            return random.randint(-1e6, 1e6)
        elif lit_type == "REAL":
            return random.uniform(-1e6, 1e6)
        elif lit_type == "TEXT":
            return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        elif lit_type == "BLOB":
            return bytes(random.getrandbits(8) for _ in range(5))
        elif lit_type == "NULL":
            return None

class Column:
    def __init__(self, table, column):
        self.table = table
        self.column = column

    def __str__(self):
        return f"{self.table}.{self.column}"

    def execute(self, schema):
        # Simulate fetching the value from the table
        return schema[self.table][self.column]


class UnaryOperator:
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __str__(self):
        return f"{self.operator} {self.expression}"

    def execute(self, schema):
        value = self.expression.execute(schema)
        if self.operator == "NOT":
            return not value
        elif self.operator == "IS NULL":
            return value is None
        elif self.operator == "IS NOT NULL":
            return value is not None
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
"""