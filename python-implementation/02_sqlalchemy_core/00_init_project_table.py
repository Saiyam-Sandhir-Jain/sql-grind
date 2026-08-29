from sqlalchemy import (
    create_engine,
    MetaData,
    Table
)

from sqlalchemy.dialects.postgresql import insert

from config import DATABASE_URL
from tables import metadata

engine = create_engine(DATABASE_URL)

employee = Table("employee", metadata, autoload_with=engine)
project = Table("project", metadata, autoload_with=engine)

stmt = insert(project).on_conflict_do_nothing()

project_data = [
    {"project_id": 1, "name": "Cloud Migration",            "cost": 150000.00,  "dept_id": 10},
    {"project_id": 2, "name": "HR Portal Revamp",           "cost": 45000.50,   "dept_id": 20},
    {"project_id": 3, "name": "Global Sales Campaign",      "cost": 85000.00,   "dept_id": 30},
    {"project_id": 4, "name": "ERP System Upgrade",         "cost": 300000.75,  "dept_id": 40},
    {"project_id": 5, "name": "AI Research Pipeline",       "cost": 500000.00,  "dept_id": 50},
    {"project_id": 6, "name": "Internal Security Audit",    "cost": 0.00,       "dept_id": 10},
    {"project_id": 7, "name": "Mobile App v2",              "cost": 120000.00,  "dept_id": 10},
    {"project_id": 8, "name": "Q4 Ad Push",                 "cost": 25000.00,   "dept_id": 30},
]

employee_stmt = insert(employee).values(
    emp_id=204,
    name="Alice",
    salary=7000,
    dept_id=10,
).on_conflict_do_nothing()

with engine.connect() as conn:
    conn.execute(stmt, project_data)
    conn.execute(employee_stmt)

print("Project seed data inserted successfully.")