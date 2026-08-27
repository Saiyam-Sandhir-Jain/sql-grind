"""
04_transactions.py

Psycopg 3 — Transactions

Topics:
    - Transactions
    - COMMIT
    - ROLLBACK
    - autocommit
    - connection transaction behavior
    - transaction context managers
    - failed transaction state
    - savepoints / nested transactions
    - isolation levels
    - ACID
"""

import psycopg

from config import DATABASE_URL


# ============================================================
# 1. BASIC TRANSACTION
# ============================================================

def basic_transaction():
    """
    Multiple statements form one logical unit of work.
    """

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.transaction():

            with conn.cursor() as cur:

                cur.execute("""
                    UPDATE employee
                    SET salary = salary + 1000
                    WHERE emp_id = 101;
                """)

                cur.execute("""
                    UPDATE employee
                    SET salary = salary + 1000
                    WHERE emp_id = 102;
                """)

        # Successful transaction context -> COMMIT

    print("Transaction committed.")


# ============================================================
# 2. ROLLBACK
# ============================================================

def rollback_example():
    """
    An exception causes the transaction context to roll back.
    """

    try:

        with psycopg.connect(DATABASE_URL) as conn:

            with conn.transaction():

                with conn.cursor() as cur:

                    cur.execute("""
                        UPDATE employee
                        SET salary = salary + 5000
                        WHERE emp_id = 101;
                    """)

                    # Simulate failure
                    raise RuntimeError("Something went wrong")

    except RuntimeError:
        print("Transaction rolled back.")


# ============================================================
# 3. EXPLICIT COMMIT / ROLLBACK
# ============================================================

def explicit_commit_rollback():
    """
    Demonstrates manual transaction control.
    """

    conn = psycopg.connect(DATABASE_URL)

    try:

        with conn.cursor() as cur:

            cur.execute("""
                UPDATE employee
                SET salary = salary + 1000
                WHERE emp_id = 101;
            """)

        conn.commit()

        print("Explicit COMMIT successful.")

    except Exception:

        conn.rollback()

        print("Explicit ROLLBACK executed.")

        raise

    finally:

        conn.close()


# ============================================================
# 4. AUTOCOMMIT
# ============================================================

def autocommit_example():
    """
    Each statement is committed independently.

    Do NOT use this for multi-step operations that must
    succeed or fail together.
    """

    with psycopg.connect(DATABASE_URL) as conn:

        conn.autocommit = True

        with conn.cursor() as cur:

            cur.execute("""
                UPDATE employee
                SET salary = salary + 100
                WHERE emp_id = 101;
            """)

            print("Statement committed independently.")


# ============================================================
# 5. FAILED TRANSACTION STATE
# ============================================================

def failed_transaction_example():
    """
    Once a statement fails inside a transaction, the transaction
    becomes aborted.

    A rollback is required before the connection can be used
    for a new transaction.
    """

    conn = psycopg.connect(DATABASE_URL)

    try:

        with conn.cursor() as cur:

            try:

                cur.execute("""
                    UPDATE employee
                    SET salary = salary + 100
                    WHERE emp_id = 101;
                """)

                # Intentionally invalid SQL
                cur.execute("""
                    THIS IS INVALID SQL;
                """)

            except Exception as error:

                print("Statement failed:")
                print(error)

                # Reset failed transaction state
                conn.rollback()

            # Connection can now be used again

            cur.execute("""
                SELECT emp_id, name, salary
                FROM employee
                WHERE emp_id = 101;
            """)

            print("Connection usable after rollback:")

            print(cur.fetchone())

    finally:

        conn.close()


# ============================================================
# 6. SAVEPOINT / NESTED TRANSACTION
# ============================================================

def savepoint_example():
    """
    Nested transaction contexts act as savepoints when already
    inside a transaction.
    """

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.transaction():

            with conn.cursor() as cur:

                # Outer transaction
                cur.execute("""
                    UPDATE employee
                    SET salary = salary + 1000
                    WHERE emp_id = 101;
                """)

                try:

                    # Inner transaction / savepoint
                    with conn.transaction():

                        cur.execute("""
                            UPDATE employee
                            SET salary = salary + 5000
                            WHERE emp_id = 102;
                        """)

                        raise RuntimeError(
                            "Simulated inner failure"
                        )

                except RuntimeError:

                    print(
                        "Inner transaction rolled back "
                        "to its savepoint."
                    )

                # Outer transaction continues
                cur.execute("""
                    UPDATE employee
                    SET salary = salary + 2000
                    WHERE emp_id = 103;
                """)

        # Outer transaction commits.


# ============================================================
# 7. ISOLATION LEVEL
# ============================================================

def serializable_transaction():
    """
    Example of running a transaction at SERIALIZABLE isolation.
    """

    with psycopg.connect(
        DATABASE_URL,
        isolation_level="serializable"
    ) as conn:

        with conn.transaction():

            with conn.cursor() as cur:

                cur.execute("""
                    SELECT emp_id, salary
                    FROM employee
                    WHERE emp_id = 101;
                """)

                print(cur.fetchone())


# ============================================================
# 8. READ COMMITTED EXPLICITLY
# ============================================================

def read_committed_transaction():
    """
    READ COMMITTED is PostgreSQL's default isolation level.
    """

    with psycopg.connect(
        DATABASE_URL,
        isolation_level="read committed"
    ) as conn:

        with conn.transaction():

            with conn.cursor() as cur:

                cur.execute("""
                    SELECT emp_id, salary
                    FROM employee
                    WHERE emp_id = 101;
                """)

                print(cur.fetchone())


# ============================================================
# 9. ACID SUMMARY
# ============================================================

def explain_acid():
    print("""
ACID

A — Atomicity
    All transaction operations succeed or none do.

C — Consistency
    Database constraints and invariants remain valid.

I — Isolation
    Concurrent transactions are controlled so their
    interactions obey the selected isolation semantics.

D — Durability
    Once committed, changes survive system failure.
""")


# ============================================================
# MAIN
# ============================================================

def main():

    explain_acid()

    # Uncomment individually while learning.

    # basic_transaction()

    # rollback_example()

    # explicit_commit_rollback()

    # autocommit_example()

    # failed_transaction_example()

    # savepoint_example()

    # read_committed_transaction()

    # serializable_transaction()


if __name__ == "__main__":
    main()