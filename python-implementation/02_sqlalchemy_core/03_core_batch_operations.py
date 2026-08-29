from sqlalchemy import create_engine, MetaData, Table, select, update, delete
from sqlalchemy.dialects.postgresql import insert
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect existing tables
employee = Table("employee", metadata, autoload_with=engine)


# ============================================================
# 1. SINGLE INSERT
# ============================================================
def single_insert(conn):
    stmt = insert(employee).values(
        emp_id=501, name="Alice", salary=70000, dept_id=10
    ).on_conflict_do_nothing()

    result = conn.execute(stmt)
    print(f"Single Insert - Rows affected: {result.rowcount}")


# ============================================================
# 2. executemany() — BATCH INSERT
# ============================================================
def batch_insert(conn):
    # Passing a list of dicts to conn.execute() triggers DBAPI executemany
    employees = [
        {"emp_id": 502, "name": "Bob", "salary": 75000, "dept_id": 20},
        {"emp_id": 503, "name": "Charlie", "salary": 65000, "dept_id": 10},
        {"emp_id": 504, "name": "David", "salary": 80000, "dept_id": 10},
    ]

    # Statement without values clause; values are supplied by parameter dicts
    stmt = insert(employee).on_conflict_do_nothing()

    result = conn.execute(stmt, employees)
    print(f"Batch Insert - Rows affected: {result.rowcount}")


# ============================================================
# 3. BATCH UPDATE
# ============================================================
def batch_update(conn):
    # Bind parameters match keys in the dictionary payload
    updates = [
        {"target_id": 502, "salary_increment": 1000},
        {"target_id": 503, "salary_increment": 2000},
        {"target_id": 504, "salary_increment": 1500},
    ]

    stmt = (
        update(employee)
        .where(employee.c.emp_id == employee.c.emp_id)  # Placeholder target
        .where(employee.c.emp_id == update.bindparams("target_id"))
        .values(salary=employee.c.salary + update.bindparams("salary_increment"))
    )

    result = conn.execute(stmt, updates)
    print(f"Batch Update - Rows affected: {result.rowcount}")


# ============================================================
# 4. BATCH DELETE
# ============================================================
def batch_delete(conn):
    deletions = [
        {"target_id": 502},
        {"target_id": 503},
        {"target_id": 504},
    ]

    stmt = delete(employee).where(employee.c.emp_id == delete.bindparams("target_id"))

    result = conn.execute(stmt, deletions)
    print(f"Batch Delete - Rows affected: {result.rowcount}")


# ============================================================
# 5. SINGLE INSERT + RETURNING
# ============================================================
def insert_returning(conn):
    stmt = (
        insert(employee)
        .values(emp_id=505, name="Eve", salary=72000, dept_id=10)
        .returning(employee.c.emp_id, employee.c.name, employee.c.salary)
        .on_conflict_do_nothing()
    )

    row = conn.execute(stmt).fetchone()
    print("\nSingle Insert Returning:", row)


# ============================================================
# 6. BATCH INSERT + RETURNING
# ============================================================
def batch_insert_returning(conn):
    employees = [
        {"emp_id": 506, "name": "Frank", "salary": 76000, "dept_id": 20},
        {"emp_id": 507, "name": "Grace", "salary": 68000, "dept_id": 10},
    ]

    stmt = (
        insert(employee)
        .returning(employee.c.emp_id, employee.c.name, employee.c.salary)
        .on_conflict_do_nothing()
    )

    # Executing batch with RETURNING yields an iterable result proxy
    result = conn.execute(stmt, employees)

    print("\nBatch INSERT RETURNING:")
    for row in result:
        print(f"  Inserted ID: {row.emp_id}, Name: {row.name}, Salary: {row.salary}")


# ============================================================
# 7. TRANSACTIONAL BATCH & ROLLBACK ON FAILURE
# ============================================================
def batch_transaction_demo():
    print("\n--- Transactional Batch with Rollback Demo ---")

    # Second item intentionally violates CHECK (salary > 0)
    bad_batch = [
        {"emp_id": 508, "name": "Hannah", "salary": 90000, "dept_id": 10},
        {"emp_id": 509, "name": "Invalid", "salary": -5000, "dept_id": 10},
    ]

    stmt = insert(employee)

    try:
        with engine.begin() as conn:
            conn.execute(stmt, bad_batch)
    except Exception as error:
        print("Batch execution failed as expected!")
        print(f"Database Error: {error.orig}")
        print("Transaction was automatically rolled back by engine.begin().")


# ============================================================
# 8. HIGH-PERFORMANCE COPY INGESTION (Psycopg 3 Integration)
# ============================================================
def demo_copy_bulk_ingest():
    print("\n--- High-Speed COPY Operations via DBAPI Connection ---")

    raw_data = [
        (601, "Bulk User 1", 95000, 10),
        (602, "Bulk User 2", 98000, 20),
        (603, "Bulk User 3", 102000, 30),
    ]

    with engine.begin() as conn:
        # Access the raw underlying Psycopg 3 connection object
        raw_psycopg_conn = conn.connection.dbapi_connection

        with raw_psycopg_conn.cursor() as cur:
            # PostgreSQL COPY FROM STDIN protocol
            copy_sql = "COPY employee (emp_id, name, salary, dept_id) FROM STDIN"
            with cur.copy(copy_sql) as copy:
                for row in raw_data:
                    copy.write_row(row)

    print(f"Successfully ingested {len(raw_data)} records via COPY protocol.")


# ============================================================
# MAIN EXECUTION ROUTINE
# ============================================================
def main():
    with engine.begin() as conn:
        single_insert(conn)
        batch_insert(conn)
        batch_update(conn)
        batch_delete(conn)
        insert_returning(conn)
        batch_insert_returning(conn)

    batch_transaction_demo()
    demo_copy_bulk_ingest()


if __name__ == "__main__":
    main()