-- INSERT INTO departments (dept_name, location, budget) VALUES
-- ('Engineering', 'Bangalore', 5000000),
-- ('Sales',       'Mumbai',    3000000),
-- ('HR',          'Bangalore', 800000),
-- ('Marketing',   'Delhi',     1500000),
-- ('Research',    'Hyderabad', 2500000);

-- -- employees: deliberate NULLs (1 no dept, 2 top-of-hierarchy no manager, 1 no email)
-- INSERT INTO employees
--   (name, email, dept_id, manager_id, salary, hire_date, job_title) VALUES
-- ('Asha Nair',      'asha@corp.com',    1, NULL, 180000, '2015-03-01', 'CTO'),
-- ('Rohit Verma',    'rohit@corp.com',   1,    1, 120000, '2016-07-15', 'Engineering Manager'),
-- ('Priya Sharma',   'priya@corp.com',   1,    2,  95000, '2018-01-10', 'Senior Engineer'),
-- ('Karan Mehta',    'karan@corp.com',   1,    2,  88000, '2019-05-20', 'Senior Engineer'),
-- ('Sneha Iyer',     'sneha@corp.com',   1,    2,  72000, '2021-02-01', 'Engineer'),
-- ('Aditya Rao',     'aditya@corp.com',  1,    2,  68000, '2021-08-11', 'Engineer'),
-- ('Meera Joshi',    'meera@corp.com',   1,    2,  61000, '2022-11-05', 'Junior Engineer'),
-- ('Vikram Singh',   'vikram@corp.com',  2, NULL, 150000, '2014-06-01', 'VP Sales'),
-- ('Neha Gupta',     'neha@corp.com',    2,    8,  92000, '2017-09-12', 'Sales Manager'),
-- ('Arjun Desai',    'arjun@corp.com',   2,    9,  67000, '2020-03-23', 'Sales Executive'),
-- ('Divya Menon',    'divya@corp.com',   2,    9,  67000, '2020-04-01', 'Sales Executive'),
-- ('Sameer Khan',    'sameer@corp.com',  2,    9,  54000, '2022-01-17', 'Sales Associate'),
-- ('Ananya Bose',    'ananya@corp.com',  3,    1,  85000, '2017-02-20', 'HR Manager'),
-- ('Rahul Pillai',   'rahul@corp.com',   3,   13,  52000, '2021-06-30', 'HR Executive'),
-- ('Ishita Kapoor',  'ishita@corp.com',  4,    1,  98000, '2016-11-11', 'Marketing Head'),
-- ('Nikhil Jain',    'nikhil@corp.com',  4,   15,  63000, '2020-08-08', 'Marketing Analyst'),
-- ('Farah Sheikh',   'farah@corp.com',   4,   15,  59000, '2022-05-19', 'Content Strategist'),
-- ('Deepak Reddy',   'deepak@corp.com',  5,    1, 110000, '2018-04-02', 'Principal Scientist'),
-- ('Tanvi Shah',     'tanvi@corp.com',   5,   18,  79000, '2021-09-27', 'Research Scientist'),
-- ('Omar Ali',       NULL,            NULL, NULL,  57000, '2023-01-09', 'Contractor');

-- INSERT INTO projects (project_name, dept_id, start_date, end_date, budget) VALUES
-- ('Payments Platform', 1, '2022-01-01', '2023-06-30', 1200000),
-- ('Mobile App Revamp', 1, '2023-02-15', NULL,          900000),
-- ('CRM Rollout',       2, '2022-05-01', '2023-01-31',  400000),
-- ('Employee Portal',   3, '2023-03-01', NULL,          150000),
-- ('Brand Campaign',    4, '2023-01-10', '2023-09-30',  600000),
-- ('LLM Prototype',     5, '2023-06-01', NULL,          750000);

-- INSERT INTO employee_projects (emp_id, project_id, hours_worked, role) VALUES
-- (2,1,320,'Lead'),    (3,1,480,'Developer'), (4,1,410,'Developer'),
-- (5,1,260,'Developer'),(3,2,300,'Lead'),     (5,2,340,'Developer'),
-- (6,2,290,'Developer'),(7,2,180,'Intern'),
-- (9,3,220,'Lead'),    (10,3,260,'Analyst'),  (11,3,240,'Analyst'),
-- (13,4,150,'Lead'),   (14,4,200,'Coordinator'),
-- (15,5,180,'Lead'),   (16,5,320,'Analyst'),  (17,5,280,'Writer'),
-- (18,6,400,'Lead'),   (19,6,360,'Researcher');

-- -- customers: Lyra Interiors and Cobalt Motors deliberately have no orders (anti-join practice)
-- INSERT INTO customers (customer_name, city, country, signup_date) VALUES
-- ('Zenith Retail',    'Mumbai',    'India',     '2021-01-15'),
-- ('Apex Traders',     'Delhi',     'India',     '2021-06-02'),
-- ('Nova Systems',     'Bangalore', 'India',     '2022-03-19'),
-- ('Orion Logistics',  'Chennai',   'India',     '2022-07-25'),
-- ('Vertex Foods',     'Pune',      'India',     '2022-11-30'),
-- ('Helios Media',     'Singapore', 'Singapore', '2023-01-08'),
-- ('Quantum Labs',     'Dubai',     'UAE',       '2023-02-14'),
-- ('Summit Apparel',   'Kolkata',   'India',     '2023-05-21'),
-- ('Lyra Interiors',   'Hyderabad', 'India',     '2023-08-03'),
-- ('Cobalt Motors',    'London',    'UK',        '2023-09-17');

-- INSERT INTO products (product_name, category, unit_price) VALUES
-- ('Laptop Pro 14',    'Electronics', 125000),
-- ('Wireless Mouse',   'Electronics',   1500),
-- ('Standing Desk',    'Furniture',    28000),
-- ('Ergonomic Chair',  'Furniture',    18000),
-- ('Monitor 27in',     'Electronics',  22000),
-- ('Notebook Pack',    'Stationery',     450),
-- ('Whiteboard',       'Stationery',    3200),
-- ('Server Rack',      'Hardware',     95000),
-- ('Network Switch',   'Hardware',     42000),
-- ('Desk Lamp',        'Furniture',     2400);

-- INSERT INTO orders (customer_id, order_date, status) VALUES
-- (1,'2023-01-12','DELIVERED'), (1,'2023-04-05','DELIVERED'),
-- (2,'2023-02-20','SHIPPED'),   (3,'2023-03-11','DELIVERED'),
-- (3,'2023-06-18','CANCELLED'), (3,'2023-09-02','PLACED'),
-- (4,'2023-04-28','DELIVERED'), (5,'2023-05-09','SHIPPED'),
-- (5,'2023-08-14','DELIVERED'), (6,'2023-06-30','DELIVERED'),
-- (7,'2023-07-07','PLACED'),    (8,'2023-08-22','DELIVERED'),
-- (1,'2023-10-01','PLACED'),    (2,'2023-10-15','SHIPPED'),
-- (4,'2023-11-03','DELIVERED');

-- INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- (1,1,2,125000),(1,2,4,1500),(1,5,2,22000),
-- (2,3,1,28000),(2,10,2,2400),
-- (3,1,1,125000),(3,4,3,18000),
-- (4,5,4,22000),(4,2,10,1500),(4,6,20,450),
-- (5,8,1,95000),
-- (6,9,2,42000),(6,7,3,3200),
-- (7,4,5,18000),(7,3,2,28000),
-- (8,1,1,125000),(8,5,1,22000),
-- (9,6,50,450),(9,2,6,1500),
-- (10,8,2,95000),(10,9,1,42000),
-- (11,7,4,3200),(11,10,3,2400),
-- (12,1,3,125000),(12,4,2,18000),(12,2,5,1500),
-- (13,5,2,22000),
-- (14,3,1,28000),(14,10,1,2400),
-- (15,9,3,42000);

-- ---------- Verify ----------
-- Expect: employees = 20, order_items = 30, employees with NULL dept_id = 1
SELECT
    (SELECT COUNT(*) FROM employees) AS employee_count,
    (SELECT COUNT(*) FROM order_items) AS order_item_count,
    (SELECT COUNT(*) FROM employees WHERE dept_id IS NULL) AS employees_no_dept;