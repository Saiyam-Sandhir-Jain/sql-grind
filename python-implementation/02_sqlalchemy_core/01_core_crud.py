from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    select,
    update,
    delete,
)
from sqlalchemy.dialects.postgresql import insert
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect existing tables
department = Table("department", metadata, autoload_with=engine)
employee = Table("employee", metadata, autoload_with=engine)

def explain_sql(stmt, title):
    """Utility to inspect generated SQL queries with parameters."""
    print(f"\n==================== {title} ====================")
    compiled = stmt.compile(engine, compile_kwargs={"literal_binds": True})
    print(f"[Generated SQL]:\n{compiled}\n")


with engine.begin() as conn:

    # ------------------------------------------------------------------
    # 1. INSERT() with parameters & ON CONFLICT
    # ------------------------------------------------------------------
    insert_stmt = (
        insert(employee)
        .values(emp_id=205, name="Grace Hopper", salary=110000, dept_id=10)
        .on_conflict_do_nothing()
    )
    explain_sql(insert_stmt, "INSERT Statement")
    conn.execute(insert_stmt)


    # ------------------------------------------------------------------
    # 2. SELECT(), WHERE(), ORDER_BY(), LIMIT()
    # ------------------------------------------------------------------
    # Selecting specific columns with conditions and ordering
    select_stmt = (
        select(employee.c.emp_id, employee.c.name, employee.c.salary)
        .where(employee.c.salary >= 80000)
        .order_by(employee.c.salary.desc())
        .limit(3)
    )
    explain_sql(select_stmt, "SELECT Statement with Filtering & Sorting")

    # Executing and exploring Result & Row objects
    result = conn.execute(select_stmt)
    print("--- Result Object Iteration (Row tuple/attribute access) ---")
    for row in result:  # row is a sqlalchemy.engine.Row
        print(f"Row tuple: {row} | Access by name: {row.name} | Access by index: {row[2]}")


    # ------------------------------------------------------------------
    # 3. MAPPINGS() - Dictionary-like Access
    # ------------------------------------------------------------------
    result_map = conn.execute(select_stmt)
    print("\n--- Result.mappings() Iteration (Key-Value dict-like) ---")
    for mapping in result_map.mappings():  # RowMapping object
        print(f"Dict output: {dict(mapping)} | Key access: {mapping['name']}")


    # ------------------------------------------------------------------
    # 4. JOIN() - Combining Tables
    # ------------------------------------------------------------------
    # Explicit JOIN between employee and department using ON clause
    join_stmt = (
        select(
            employee.c.name.label("employee_name"),
            department.c.name.label("department_name")
        )
        .select_from(
            employee.join(department, employee.c.dept_id == department.c.dept_id)
        )
        .where(department.c.dept_id == 10)
    )
    explain_sql(join_stmt, "JOIN Statement")
    
    join_results = conn.execute(join_stmt).mappings().fetchall()
    print("--- Joined Results ---")
    for row in join_results:
        print(f"Employee: {row['employee_name']} -> Dept: {row['department_name']}")


    # ------------------------------------------------------------------
    # 5. UPDATE() with parameterized values
    # ------------------------------------------------------------------
    update_stmt = (
        update(employee)
        .where(employee.c.emp_id == 205)
        .values(salary=125000)
    )
    explain_sql(update_stmt, "UPDATE Statement")
    conn.execute(update_stmt)


    # ------------------------------------------------------------------
    # 6. DELETE()
    # ------------------------------------------------------------------
    delete_stmt = (
        delete(employee)
        .where(employee.c.emp_id == 205)
    )
    explain_sql(delete_stmt, "DELETE Statement")
    conn.execute(delete_stmt)