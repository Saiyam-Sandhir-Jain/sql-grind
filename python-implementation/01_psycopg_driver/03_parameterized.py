"""
03_parameterized.py

Psycopg 3 — Parameterized SQL and SQL Composition

Topics demonstrated:
    1. Unsafe SQL construction
    2. SQL injection
    3. Positional parameters
    4. Named parameters
    5. Values vs identifiers
    6. Dynamic identifiers with psycopg.sql.Identifier
    7. SQL composition
    8. Safe dynamic ORDER BY
    9. Safe dynamic table selection
    10. Python <-> PostgreSQL parameter adaptation

IMPORTANT:
    The unsafe examples are intentionally constructed as strings for teaching.
    They are NOT executed against PostgreSQL.
"""

import psycopg
from psycopg import sql

from config import DATABASE_URL


# ============================================================
# 1. UNSAFE SQL — STRING CONCATENATION
# ============================================================

def unsafe_concatenation(cur, name):
    """
    ❌ NEVER construct SQL this way with untrusted input.
    """

    query = (
        "SELECT emp_id, name, salary "
        "FROM employee "
        "WHERE name = '" + name + "'"
    )

    print("\n[UNSAFE - CONCATENATION]")
    print(query)

    # Deliberately NOT executed.
    #
    # cur.execute(query)


# ============================================================
# 2. UNSAFE SQL — F-STRING
# ============================================================

def unsafe_f_string(cur, name):
    """
    ❌ NEVER interpolate untrusted values directly into SQL.
    """

    query = f"""
        SELECT emp_id, name, salary
        FROM employee
        WHERE name = '{name}'
    """

    print("\n[UNSAFE - F-STRING]")
    print(query)

    # Deliberately NOT executed.
    #
    # cur.execute(query)


# ============================================================
# 3. UNSAFE SQL — PYTHON % FORMATTING
# ============================================================

def unsafe_percent_formatting(cur, name):
    """
    ❌ This is Python string formatting.
       It is NOT Psycopg parameterization.
    """

    query = """
        SELECT emp_id, name, salary
        FROM employee
        WHERE name = '%s'
    """ % name

    print("\n[UNSAFE - PYTHON % FORMATTING]")
    print(query)

    # Deliberately NOT executed.
    #
    # cur.execute(query)


# ============================================================
# 4. SQL INJECTION EXAMPLE
# ============================================================

def demonstrate_injection():
    """
    Demonstrates how unsafe string construction can change SQL logic.

    We only construct and print the malicious SQL.
    We DO NOT execute it.
    """

    malicious_name = "' OR '1'='1"

    unsafe_query = f"""
        SELECT emp_id, name, salary
        FROM employee
        WHERE name = '{malicious_name}'
    """

    print("\n" + "=" * 60)
    print("SQL INJECTION DEMONSTRATION")
    print("=" * 60)

    print("\nAttacker-controlled value:")
    print(repr(malicious_name))

    print("\nResulting UNSAFE SQL:")
    print(unsafe_query)

    print(
        "\nThe attacker has injected SQL syntax into the query "
        "instead of supplying only a data value."
    )

    # NEVER execute this:
    #
    # cur.execute(unsafe_query)


# ============================================================
# 5. SAFE — POSITIONAL PARAMETERS
# ============================================================

def positional_parameter(cur, name):
    """
    ✅ Safe parameterized query.

    %s is a Psycopg placeholder.
    It is NOT Python string formatting.
    """

    query = """
        SELECT emp_id, name, salary
        FROM employee
        WHERE name = %s
    """

    cur.execute(query, (name,))

    rows = cur.fetchall()

    print("\n[SAFE - POSITIONAL PARAMETER]")

    for row in rows:
        print(row)


# ============================================================
# 6. SAFE — MULTIPLE POSITIONAL PARAMETERS
# ============================================================

def multiple_positional_parameters(cur, dept_id, minimum_salary):
    """
    Multiple positional parameters.

    First %s  -> dept_id
    Second %s -> minimum_salary
    """

    query = """
        SELECT emp_id, name, salary, dept_id
        FROM employee
        WHERE dept_id = %s
          AND salary >= %s
        ORDER BY salary DESC
    """

    cur.execute(
        query,
        (dept_id, minimum_salary),
    )

    rows = cur.fetchall()

    print("\n[SAFE - MULTIPLE POSITIONAL PARAMETERS]")

    for row in rows:
        print(row)


# ============================================================
# 7. SAFE — NAMED PARAMETERS
# ============================================================

def named_parameters(cur, dept_id, minimum_salary):
    """
    Named parameters are useful when a query has many parameters.

    %(dept_id)s
    %(minimum_salary)s
    """

    query = """
        SELECT emp_id, name, salary, dept_id
        FROM employee
        WHERE dept_id = %(dept_id)s
          AND salary >= %(minimum_salary)s
        ORDER BY salary DESC
    """

    parameters = {
        "dept_id": dept_id,
        "minimum_salary": minimum_salary,
    }

    cur.execute(query, parameters)

    rows = cur.fetchall()

    print("\n[SAFE - NAMED PARAMETERS]")

    for row in rows:
        print(row)


# ============================================================
# 8. WHY %s IS NOT PYTHON FORMATTING
# ============================================================

def explain_percent_placeholder(cur, name):
    """
    Demonstrates the correct Psycopg use of %s.

    DO NOT do:

        query = "SELECT ... WHERE name = '%s'" % name

    Instead do:

        cur.execute(query, (name,))
    """

    query = """
        SELECT emp_id, name
        FROM employee
        WHERE name = %s
    """

    cur.execute(query, (name,))

    print("\n[%s IS A PSYCOPG PARAMETER PLACEHOLDER]")

    for row in cur:
        print(row)


# ============================================================
# 9. SAFE PARAMETERS PROTECT VALUES
# ============================================================

def safe_malicious_value(cur):
    """
    The malicious-looking string is treated as DATA.

    It does not become SQL syntax.
    """

    malicious_name = "' OR '1'='1"

    query = """
        SELECT emp_id, name, salary
        FROM employee
        WHERE name = %s
    """

    cur.execute(query, (malicious_name,))

    rows = cur.fetchall()

    print("\n[SAFE - MALICIOUS VALUE AS DATA]")

    print("Rows returned:", rows)

    print(
        "\nThe malicious string was supplied as a value, "
        "not inserted into the SQL statement."
    )


# ============================================================
# 10. VALUES vs IDENTIFIERS
# ============================================================

def explain_values_vs_identifiers():
    """
    VERY IMPORTANT:

    Parameters are for VALUES.

    Parameters are NOT for SQL identifiers such as:
        - table names
        - column names
    """

    print("\n" + "=" * 60)
    print("VALUES vs IDENTIFIERS")
    print("=" * 60)

    print(
        """
VALUES:
    employee_id
    name
    salary
    date
    department_id

Use:
    %s
    %(name)s

IDENTIFIERS:
    employee
    employee_id
    salary

Use:
    psycopg.sql.Identifier(...)
"""
    )


# ============================================================
# 11. WRONG — PARAMETER AS COLUMN NAME
# ============================================================

def wrong_dynamic_column(cur, column_name):
    """
    ❌ This does NOT safely mean:

        ORDER BY salary

    %s is for a value, not an identifier.
    """

    query = """
        SELECT emp_id, name, salary
        FROM employee
        ORDER BY %s
    """

    print("\n[WRONG - PARAMETER USED AS IDENTIFIER]")
    print("Requested column:", column_name)

    # Do NOT rely on this to dynamically select a column.
    #
    # cur.execute(query, (column_name,))


# ============================================================
# 12. SAFE DYNAMIC IDENTIFIER — sql.Identifier
# ============================================================

def safe_dynamic_column(cur, column_name):
    """
    ✅ sql.Identifier() is used when a dynamic SQL identifier
       is genuinely required.

    Example:

        column_name = "salary"

    becomes conceptually:

        ORDER BY "salary"
    """

    query = sql.SQL("""
        SELECT emp_id, name, salary
        FROM employee
        ORDER BY {}
    """).format(
        sql.Identifier(column_name)
    )

    print("\n[SAFE - DYNAMIC IDENTIFIER]")
    print("Column:", column_name)

    cur.execute(query)

    for row in cur:
        print(row)


# ============================================================
# 13. DYNAMIC IDENTIFIER + WHITELIST
# ============================================================

def safe_dynamic_sort(cur, requested_sort):
    """
    Best practice:

    Do not blindly accept arbitrary identifiers from a user.

    First map application-level choices to known database columns.
    """

    allowed_columns = {
        "id": "emp_id",
        "name": "name",
        "salary": "salary",
        "department": "dept_id",
    }

    if requested_sort not in allowed_columns:
        raise ValueError("Invalid sort option")

    actual_column = allowed_columns[requested_sort]

    query = sql.SQL("""
        SELECT emp_id, name, salary, dept_id
        FROM employee
        ORDER BY {}
    """).format(
        sql.Identifier(actual_column)
    )

    print("\n[SAFE - WHITELISTED DYNAMIC SORT]")
    print("Requested:", requested_sort)
    print("Database column:", actual_column)

    cur.execute(query)

    for row in cur:
        print(row)


# ============================================================
# 14. SAFE DYNAMIC TABLE NAME
# ============================================================

def safe_dynamic_table(cur, table_name):
    """
    Dynamic table names are identifiers.

    Therefore use sql.Identifier().
    """

    allowed_tables = {
        "employee": "employee",
        "department": "department",
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid table")

    actual_table = allowed_tables[table_name]

    query = sql.SQL(
        "SELECT * FROM {}"
    ).format(
        sql.Identifier(actual_table)
    )

    print("\n[SAFE - DYNAMIC TABLE]")
    print("Table:", actual_table)

    cur.execute(query)

    for row in cur:
        print(row)


# ============================================================
# 15. SQL COMPOSITION
# ============================================================

def sql_composition_example(cur, column_name):
    """
    sql.SQL() represents the SQL structure.

    sql.Identifier() represents an identifier.

    .format() combines them safely.
    """

    query = sql.SQL("""
        SELECT {}
        FROM employee
    """).format(
        sql.Identifier(column_name)
    )

    print("\n[SQL COMPOSITION]")
    print(query)

    cur.execute(query)

    for row in cur:
        print(row)


# ============================================================
# 16. COMBINING IDENTIFIERS AND PARAMETERS
# ============================================================

def identifier_plus_value(cur, column_name, minimum_value):
    """
    This demonstrates the important distinction:

        Identifier -> sql.Identifier()
        Value      -> %s parameter
    """

    query = sql.SQL("""
        SELECT emp_id, name, salary
        FROM employee
        WHERE {} >= %s
    """).format(
        sql.Identifier(column_name)
    )

    cur.execute(
        query,
        (minimum_value,)
    )

    print("\n[IDENTIFIER + PARAMETERIZED VALUE]")

    for row in cur:
        print(row)


# ============================================================
# 17. sql.Literal — TEACHING EXAMPLE
# ============================================================

def literal_example():
    """
    Psycopg also provides sql.Literal() for embedding a literal
    into composed SQL.

    However, for normal runtime data values, parameters are
    generally preferable.
    """

    name = "Alice"

    query = sql.SQL("""
        SELECT *
        FROM employee
        WHERE name = {}
    """).format(
        sql.Literal(name)
    )

    print("\n[sql.Literal EXAMPLE]")
    print(query)

    print(
        "\nFor ordinary runtime values, prefer %s parameters."
    )


# ============================================================
# 18. PYTHON -> POSTGRESQL TYPE ADAPTATION
# ============================================================

def type_adaptation(cur):
    """
    Psycopg adapts Python values to PostgreSQL values.

    Examples:
        int
        str
        bool
        None
    """

    employee_id = 101
    name = "Alice"
    active = True

    query = """
        SELECT
            %s AS employee_id,
            %s AS employee_name,
            %s AS is_active,
            %s AS null_value
    """

    cur.execute(
        query,
        (
            employee_id,
            name,
            active,
            None,
        )
    )

    row = cur.fetchone()

    print("\n[PYTHON -> POSTGRESQL TYPE ADAPTATION]")
    print(row)

    print("Python types:")
    print(type(row[0]))
    print(type(row[1]))
    print(type(row[2]))
    print(type(row[3]))


# ============================================================
# 19. COMPLETE DEMONSTRATION
# ============================================================

def main():

    # --------------------------------------------------------
    # These demonstrations do not need a database connection.
    # --------------------------------------------------------

    demonstrate_injection()

    explain_values_vs_identifiers()

    literal_example()

    # --------------------------------------------------------
    # Database demonstrations
    # --------------------------------------------------------

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            # ------------------------------------------------
            # SAFE VALUE PARAMETERS
            # ------------------------------------------------

            positional_parameter(
                cur,
                "Alice"
            )

            multiple_positional_parameters(
                cur,
                dept_id=10,
                minimum_salary=70000
            )

            named_parameters(
                cur,
                dept_id=10,
                minimum_salary=70000
            )

            explain_percent_placeholder(
                cur,
                "Alice"
            )

            # ------------------------------------------------
            # SQL INJECTION — SAFE VERSION
            # ------------------------------------------------

            safe_malicious_value(cur)

            # ------------------------------------------------
            # IDENTIFIERS
            # ------------------------------------------------

            # Demonstration of the concept.
            # Uncomment only if your employee table exists.

            # safe_dynamic_column(cur, "salary")

            # safe_dynamic_sort(cur, "salary")

            # safe_dynamic_table(cur, "employee")

            # sql_composition_example(
            #     cur,
            #     "salary"
            # )

            # identifier_plus_value(
            #     cur,
            #     "salary",
            #     70000
            # )

            # ------------------------------------------------
            # TYPE ADAPTATION
            # ------------------------------------------------

            type_adaptation(cur)

            # ------------------------------------------------
            # UNSAFE EXAMPLES
            # ------------------------------------------------
            #
            # These only PRINT the dangerous SQL.
            # They intentionally do NOT execute it.

            unsafe_concatenation(
                cur,
                "Alice"
            )

            unsafe_f_string(
                cur,
                "Alice"
            )

            unsafe_percent_formatting(
                cur,
                "Alice"
            )


if __name__ == "__main__":
    main()