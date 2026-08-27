DROP TABLE IF EXISTS department, employee;

CREATE TABLE department (
    dept_id INTEGER PRIMARY KEY,
    name    TEXT    NOT NULL
);

CREATE TABLE employee (
    emp_id  INTEGER PRIMARY KEY,
    name    TEXT    NOT NULL,
    salary  INTEGER CHECK (salary > 0),
    dept_id INTEGER NOT NULL REFERENCES department(dept_id)
);