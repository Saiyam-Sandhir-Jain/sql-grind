import psycopg
from config import DATABASE_URL

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO department (dept_id, name) VALUES
            (10, 'Engineering'),
            (20, 'Human Resources'),
            (30, 'Sales'),
            (40, 'Finance'),
            (50, 'Research & Development');

            INSERT INTO employee (emp_id, name, salary, dept_id) VALUES
            (101, 'Alice Smith', 95000, 10),
            (102, 'Bob Jones', 62000, 20),
            (103, 'Charlie Brown', 88000, 10),
            (104, 'Diana Prince', 105000, 40),
            (105, 'Evan Wright', 1, 30),
            (106, 'Fiona Gallagher', 75000, 10),
            (107, 'George Clark', 82000, 10),
            (108, 'Hannah Abbott', 58000, 20),
            (109, 'Ian Malcolm', 250000, 50),
            (110, 'Julia Roberts', 91000, 30);
        """)

        cur.execute("SELECT COUNT(*) FROM department;")
        department_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM employee;")
        employee_count = cur.fetchone()[0]

        print(f"Successfully inserted rows!\nTotal departments: {department_count}\nTotal employees: {employee_count}")