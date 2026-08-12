DROP TABLE IF EXISTS order_items, orders, products, customers, employee_projects, projects, employees, departments CASCADE;

CREATE TABLE departments (
    dept_id     SERIAL PRIMARY KEY,
    dept_name   VARCHAR(50) NOT NULL UNIQUE,
    location    VARCHAR(50),
    budget      NUMERIC(12, 2) CHECK (budget >= 0)
);

CREATE TABLE employees (
    emp_id      SERIAL PRIMARY KEY,
    name        VARCHAR(80) NOT NULL,
    email       VARCHAR(120) UNIQUE,
    dept_id     INT REFERENCES departments(dept_id),
    manager_id  INT REFERENCES employees(emp_id),
    salary      NUMERIC(10, 2) CHECK (salary > 0),
    hire_date   DATE NOT NULL,
    job_title   VARCHAR(60)
);

CREATE TABLE projects (
    project_id      SERIAL PRIMARY KEY,
    project_name    VARCHAR(80) NOT NULL,
    dept_id         INT REFERENCES departments(dept_id),
    start_date      DATE,
    end_date        DATE,
    budget          NUMERIC(12, 2),

    CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE TABLE employee_projects (
    emp_id          INT REFERENCES employees(emp_id),
    project_id      INT REFERENCES projects(project_id),
    hours_worked    INT DEFAULT 0 CHECK (hours_worked >= 0),
    role            VARCHAR(40),

    PRIMARY KEY (emp_id, project_id)
);

CREATE TABLE customers (
    customer_id     SERIAL PRIMARY KEY,
    customer_name   VARCHAR(80) NOT NULL,
    city            VARCHAR(50),
    country         VARCHAR(50),
    signup_date     DATE
);

CREATE TABLE products (
    product_id      SERIAL PRIMARY KEY,
    product_name    VARCHAR(80) NOT NULL,
    category        VARCHAR(40),
    unit_price      NUMERIC(10, 2) CHECK (unit_price >= 0)
);

CREATE TABLE orders (
    order_id        SERIAL PRIMARY KEY,
    customer_id     INT REFERENCES customers(customer_id),
    order_date      DATE NOT NULL,
    status          VARCHAR(20) DEFAULT 'PLACED',

    CHECK (status IN ('PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED'))
);

CREATE TABLE order_items (
    order_id    INT REFERENCES orders(order_id),
    product_id  INT REFERENCES products(product_id),
    quantity    INT NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),

    PRIMARY KEY (order_id, product_id)
);