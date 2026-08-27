"""
06_connection_pool.py

Psycopg 3 — Connection Pooling

Topics:
    - Why connection pooling exists
    - Connection creation cost
    - Concurrency
    - Pool sizing
    - Borrowing connections
    - Returning connections
    - psycopg_pool
    - Pool lifecycle
    - Transactions with pooled connections
    - Pool exhaustion
    - Common mistakes
"""

from psycopg_pool import ConnectionPool

from config import DATABASE_URL


# ============================================================
# 1. CREATE A CONNECTION POOL
# ============================================================

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=2,
    max_size=10,
)


# ============================================================
# 2. BORROW A CONNECTION
# ============================================================

def fetch_employees():

    with pool.connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT emp_id, name, salary, dept_id
                FROM employee
                ORDER BY emp_id
            """)

            rows = cur.fetchall()

            return rows


# ============================================================
# 3. PARAMETERIZED QUERY USING POOLED CONNECTION
# ============================================================

def fetch_employee(emp_id):

    with pool.connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT emp_id, name, salary, dept_id
                FROM employee
                WHERE emp_id = %s
                """,
                (emp_id,)
            )

            return cur.fetchone()


# ============================================================
# 4. TRANSACTION USING POOLED CONNECTION
# ============================================================

def give_raise(emp_id, amount):

    with pool.connection() as conn:

        with conn.transaction():

            with conn.cursor() as cur:

                cur.execute(
                    """
                    UPDATE employee
                    SET salary = salary + %s
                    WHERE emp_id = %s
                    """,
                    (amount, emp_id)
                )

                print(
                    "Rows updated:",
                    cur.rowcount
                )

        # Successful transaction -> COMMIT
        #
        # Connection is then returned to pool.


# ============================================================
# 5. TRANSACTION ROLLBACK
# ============================================================

def failed_transaction(emp_id):

    try:

        with pool.connection() as conn:

            with conn.transaction():

                with conn.cursor() as cur:

                    cur.execute(
                        """
                        UPDATE employee
                        SET salary = salary + 5000
                        WHERE emp_id = %s
                        """,
                        (emp_id,)
                    )

                    # Simulate failure
                    raise RuntimeError(
                        "Simulated transaction failure"
                    )

    except RuntimeError:

        print(
            "Transaction rolled back."
        )


# ============================================================
# 6. POOL SIZING INFORMATION
# ============================================================

def explain_pool_sizing():

    print("""
POOL SIZING

min_size:
    Baseline number of connections managed by the pool.

max_size:
    Maximum pool capacity.

Important:
    max_size is per application process.

Example:

    4 application workers
    max_size = 10

Potential total:
    4 × 10 = 40 connections

Therefore pool sizing must consider:

    - PostgreSQL max_connections
    - number of application workers
    - other applications
    - query duration
    - database CPU / I/O
    - expected concurrency
""")


# ============================================================
# 7. COMMON MISTAKES
# ============================================================

def explain_common_mistakes():

    print("""
COMMON POOLING MISTAKES

1. Creating a new pool for every request.

2. Holding a connection while doing slow non-database work.

3. Forgetting to return connections.

4. Making the pool unnecessarily large.

5. Assuming a pooled connection is a brand-new session.

6. Leaving transactions/session state behind.

7. Thinking pooling automatically makes slow SQL fast.

8. Ignoring total pool size across multiple workers.
""")


# ============================================================
# 8. POOL LIFECYCLE
# ============================================================

def explain_lifecycle():

    print("""
POOL LIFECYCLE

Application starts
        ↓
Create pool
        ↓
Request arrives
        ↓
Borrow connection
        ↓
Execute SQL
        ↓
Commit / rollback
        ↓
Return connection
        ↓
Next request reuses it
        ↓
Application shuts down
        ↓
Close pool
""")


# ============================================================
# 9. CLOSE POOL
# ============================================================

def close_pool():

    pool.close()

    print(
        "Connection pool closed."
    )


# ============================================================
# 10. MAIN
# ============================================================

def main():

    explain_pool_sizing()

    explain_common_mistakes()

    explain_lifecycle()

    # --------------------------------------------------------
    # Database examples
    # --------------------------------------------------------
    #
    # Uncomment while testing.
    #
    # print(fetch_employees())
    #
    # print(fetch_employee(101))
    #
    # give_raise(101, 1000)
    #
    # failed_transaction(101)
    #
    # --------------------------------------------------------
    # Close pool when application shuts down.
    # --------------------------------------------------------
    #
    # close_pool()


if __name__ == "__main__":
    main()