from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect existing tables
department = Table("department", metadata, autoload_with=engine)
employee = Table("employee", metadata, autoload_with=engine)
project = Table("project", metadata, autoload_with=engine)


# ======================================================================
# 1. MANUAL TRANSACTION MANAGEMENT (engine.connect)
# ======================================================================
# "Commit as you go" style. You must call trans.commit() or trans.rollback()
print("\n=== 1. Testing Manual Transaction (engine.connect) ===")

with engine.connect() as conn:
    trans = conn.begin()  # Explicitly start transaction block
    try:
        emp_stmt = (
            insert(employee)
            .values(emp_id=301, name="Linus Torvalds", salary=150000, dept_id=10)
            .on_conflict_do_nothing()
        )
        conn.execute(emp_stmt)

        trans.commit()  # Explicit commit
        print("[Manual Transaction]: Changes committed successfully.")
    except Exception as e:
        trans.rollback()  # Explicit rollback
        print(f"[Manual Transaction]: Rolled back due to error: {e}")


# ======================================================================
# 2. AUTOMATIC TRANSACTION SCOPE (engine.begin)
# ======================================================================
# "Begin once" style. Starts a transaction block automatically:
# - Commits on clean exit.
# - Rolls back automatically if an unhandled exception is raised.
print("\n=== 2. Testing Automatic Scope Success (engine.begin) ===")

project_data = [
    {"project_id": 1, "name": "Cloud Migration",         "cost": 150000.00, "dept_id": 10},
    {"project_id": 2, "name": "HR Portal Revamp",        "cost": 45000.50,  "dept_id": 20},
    {"project_id": 3, "name": "Global Sales Campaign",   "cost": 85000.00,  "dept_id": 30},
    {"project_id": 4, "name": "ERP System Upgrade",      "cost": 300000.75, "dept_id": 40},
    {"project_id": 5, "name": "AI Research Pipeline",    "cost": 500000.00, "dept_id": 50},
    {"project_id": 6, "name": "Internal Security Audit", "cost": 0.00,      "dept_id": 10},
    {"project_id": 7, "name": "Mobile App v2",           "cost": 120000.00, "dept_id": 10},
    {"project_id": 8, "name": "Q4 Ad Push",              "cost": 25000.00,  "dept_id": 30},
]

with engine.begin() as conn:
    stmt = insert(project).on_conflict_do_nothing()
    conn.execute(stmt, project_data)
    print("[Auto Transaction]: Projects inserted and committed automatically.")


# ======================================================================
# 3. SAVEPOINTS / NESTED TRANSACTIONS (conn.begin_nested)
# ======================================================================
# Isolates inner failures without forcing a rollback of the whole transaction.
# - conn.begin_nested() creates a SAVEPOINT
# - savepoint.rollback() executes "ROLLBACK TO SAVEPOINT"
print("\n=== 3. Testing SAVEPOINTs with conn.begin_nested() ===")

with engine.begin() as conn:  # Outer transaction starts (BEGIN)
    
    # Outer Step A: Valid record
    conn.execute(
        insert(employee)
        .values(emp_id=401, name="Valid Employee 1", salary=85000, dept_id=10)
        .on_conflict_do_nothing()
    )
    print("[Main Transaction]: Inserted emp_id 401.")

    # Create Savepoint Marker
    savepoint = conn.begin_nested()  # SAVEPOINT sa_savepoint_1
    print("[Savepoint]: Created savepoint checkpoint.")

    try:
        # Outer Step B: Invalid record (Fails CHECK constraint: salary > 0)
        conn.execute(
            insert(employee).values(
                emp_id=402, name="Invalid Employee", salary=-5000, dept_id=10
            )
        )
        savepoint.commit()
    except DBAPIError:
        print("[Savepoint]: Constraint failed! Rolling back ONLY to savepoint...")
        savepoint.rollback()  # ROLLBACK TO SAVEPOINT sa_savepoint_1

    # Outer Step C: Valid record (Main transaction continues despite step B failing)
    conn.execute(
        insert(employee)
        .values(emp_id=403, name="Valid Employee 2", salary=92000, dept_id=20)
        .on_conflict_do_nothing()
    )
    print("[Main Transaction]: Inserted emp_id 403.")


# ======================================================================
# 4. VERIFICATION OF SAVEPOINT BEHAVIOR
# ======================================================================
print("\n=== 4. Savepoint Final Database Verification ===")

with engine.connect() as conn:
    results = conn.execute(
        select(employee.c.emp_id, employee.c.name).where(
            employee.c.emp_id.in_([401, 402, 403])
        )
    ).fetchall()

    for row in results:
        print(f"Persisted in PostgreSQL -> ID: {row.emp_id}, Name: {row.name}")