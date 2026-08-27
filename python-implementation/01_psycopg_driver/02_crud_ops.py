import psycopg

from config import DATABASE_URL

def print_table(curr, query, params=None, title="Query Results"):
    cur.execute(query, params or ())
    rows = cur.fetchall()

    print(f"\n--- {title} ---")
    if not rows:
        print("No rows found.")
        return

    for row in rows:
        print(row)


with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:

        # READ
        print_table(
            cur,
            """
            SELECT emp_id, name, salary
            FROM employee
            ORDER BY emp_id;
            """,
            title="All Employees",
        )

        # INSERT
        cur.execute("""
            INSERT INTO employee 
                (emp_id, name, salary, dept_id)
            VALUES
                (111, 'Test Employee1', 70000, 10),
                (112, 'Test Employee2', 80001, 10)
            ON CONFLICT (emp_id) DO NOTHING;
            -- RETURNING emp_id, name, salary, dept_id
        """)

        print_table(
            cur,
            """
            SELECT *
            FROM employee
            WHERE name LIKE 'Test Employee_'
            ORDER BY emp_id;
            """,
            title="Insert 2 new employees",
        )

        print(f"Rows affected: {cur.rowcount}")

        # UPDATE
        print("\n--- Update rows ---")

        cur.execute("""
            UPDATE employee
            SET salary = salary + 2
            WHERE emp_id = 101;
            -- RETURNING emp_id, name, salary
        """)

        print(f"Rows affected: {cur.rowcount}")

        # DELETE
        print_table(
            cur,
            """
            DELETE FROM employee
            WHERE emp_id IN (111, 112)
            RETURNING emp_id, name, salary;
            """,
            title="Delete rows",
        )

        print("Deleted rows:", cur.rowcount)