"""
05_batch_operations.py

Psycopg 3 — Batch Operations

Topics:
    - execute()
    - executemany()
    - batch INSERT
    - batch UPDATE
    - batch DELETE
    - rowcount
    - RETURNING
    - executemany(returning=True)
    - cur.results()
    - transactions around batches
    - performance considerations
"""

import psycopg

from config import DATABASE_URL


# ============================================================
# 1. execute() — SINGLE OPERATION
# ============================================================

def single_insert(conn):

    with conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO employee
                (name, salary, dept_id)
            VALUES (%s, %s, %s)
            """,
            ("Alice", 70000, 10)
        )

        print("Rows affected:", cur.rowcount)


# ============================================================
# 2. executemany() — BATCH INSERT
# ============================================================

def batch_insert(conn):

    employees = [
        ("Alice", 70000, 10),
        ("Bob", 75000, 20),
        ("Charlie", 65000, 10),
    ]

    with conn.cursor() as cur:

        cur.executemany(
            """
            INSERT INTO employee
                (name, salary, dept_id)
            VALUES (%s, %s, %s)
            """,
            employees
        )

        print("Rows affected:", cur.rowcount)


# ============================================================
# 3. BATCH UPDATE
# ============================================================

def batch_update(conn):

    updates = [
        (1000, 101),
        (2000, 102),
        (1500, 103),
    ]

    with conn.cursor() as cur:

        cur.executemany(
            """
            UPDATE employee
            SET salary = salary + %s
            WHERE emp_id = %s
            """,
            updates
        )

        print("Rows affected:", cur.rowcount)


# ============================================================
# 4. BATCH DELETE
# ============================================================

def batch_delete(conn):

    employee_ids = [
        (101,),
        (102,),
        (103,),
    ]

    with conn.cursor() as cur:

        cur.executemany(
            """
            DELETE FROM employee
            WHERE emp_id = %s
            """,
            employee_ids
        )

        print("Rows affected:", cur.rowcount)


# ============================================================
# 5. SINGLE INSERT + RETURNING
# ============================================================

def insert_returning(conn):

    with conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO employee
                (name, salary, dept_id)
            VALUES (%s, %s, %s)
            RETURNING emp_id, name, salary
            """,
            ("David", 80000, 10)
        )

        row = cur.fetchone()

        print("\nInserted row:")
        print(row)


# ============================================================
# 6. UPDATE + RETURNING
# ============================================================

def update_returning(conn):

    with conn.cursor() as cur:

        cur.execute(
            """
            UPDATE employee
            SET salary = salary + %s
            WHERE emp_id = %s
            RETURNING emp_id, name, salary
            """,
            (1000, 101)
        )

        row = cur.fetchone()

        print("\nUpdated row:")
        print(row)


# ============================================================
# 7. DELETE + RETURNING
# ============================================================

def delete_returning(conn):

    with conn.cursor() as cur:

        cur.execute(
            """
            DELETE FROM employee
            WHERE emp_id = %s
            RETURNING emp_id, name, salary
            """,
            (101,)
        )

        row = cur.fetchone()

        print("\nDeleted row:")
        print(row)


# ============================================================
# 8. executemany(returning=True)
# ============================================================

def batch_insert_returning(conn):

    employees = [
        ("Eve", 72000, 10),
        ("Frank", 76000, 20),
        ("Grace", 68000, 10),
    ]

    with conn.cursor() as cur:

        cur.executemany(
            """
            INSERT INTO employee
                (name, salary, dept_id)
            VALUES (%s, %s, %s)
            RETURNING emp_id, name, salary
            """,
            employees,
            returning=True
        )

        print("\nBatch INSERT RETURNING:")

        for result in cur.results():

            rows = result.fetchall()

            for row in rows:
                print(row)


# ============================================================
# 9. BATCH UPDATE + RETURNING
# ============================================================

def batch_update_returning(conn):

    updates = [
        (500, 101),
        (1000, 102),
        (1500, 103),
    ]

    with conn.cursor() as cur:

        cur.executemany(
            """
            UPDATE employee
            SET salary = salary + %s
            WHERE emp_id = %s
            RETURNING emp_id, name, salary
            """,
            updates,
            returning=True
        )

        print("\nBatch UPDATE RETURNING:")

        for result in cur.results():

            rows = result.fetchall()

            for row in rows:
                print(row)


# ============================================================
# 10. BATCH TRANSACTION
# ============================================================

def transactional_batch():

    employees = [
        ("Alice", 70000, 10),
        ("Bob", 75000, 20),
        ("Charlie", 65000, 10),
    ]

    with psycopg.connect(DATABASE_URL) as conn:

        try:

            with conn.transaction():

                with conn.cursor() as cur:

                    cur.executemany(
                        """
                        INSERT INTO employee
                            (name, salary, dept_id)
                        VALUES (%s, %s, %s)
                        """,
                        employees
                    )

                    print(
                        "Batch executed:",
                        cur.rowcount,
                        "rows"
                    )

            print("Transaction committed.")

        except Exception as error:

            print("Batch failed.")
            print("Transaction rolled back.")
            print(error)


# ============================================================
# 11. BATCH WITH FAILURE
# ============================================================

def batch_failure_demo():

    employees = [
        ("Alice", 70000, 10),
        ("Bob", 75000, 20),

        # Deliberately invalid data example.
        # Adjust depending on your schema.
        (None, 65000, 10),
    ]

    with psycopg.connect(DATABASE_URL) as conn:

        try:

            with conn.transaction():

                with conn.cursor() as cur:

                    cur.executemany(
                        """
                        INSERT INTO employee
                            (name, salary, dept_id)
                        VALUES (%s, %s, %s)
                        """,
                        employees
                    )

        except Exception as error:

            print("\nBatch failed:")
            print(error)

            print(
                "The transaction was rolled back."
            )


# ============================================================
# 12. PERFORMANCE CONCEPT
# ============================================================

def explain_performance():

    print("""
PERFORMANCE

execute():

    One SQL statement
    + one parameter set


executemany():

    One SQL template
    + many parameter sets


For large-scale bulk loading:

    Consider PostgreSQL COPY.


Remember:

    executemany()
        !=
    one giant INSERT statement

and:

    executemany()
        !=
    transaction batching
""")


# ============================================================
# MAIN
# ============================================================

def main():

    explain_performance()

    # Uncomment ONE demonstration at a time.

    # transactional_batch()

    # batch_failure_demo()

    # with psycopg.connect(DATABASE_URL) as conn:
    #
    #     with conn.transaction():
    #
    #         batch_insert(conn)

    # with psycopg.connect(DATABASE_URL) as conn:
    #
    #     with conn.transaction():
    #
    #         insert_returning(conn)

    # with psycopg.connect(DATABASE_URL) as conn:
    #
    #     with conn.transaction():
    #
    #         batch_insert_returning(conn)


if __name__ == "__main__":
    main()