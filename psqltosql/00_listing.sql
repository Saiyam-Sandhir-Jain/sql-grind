-- psql meta command for listing database: \l
-- SQL Equivalent
SELECT datname AS database_name
FROM pg_database -- pg_database is a system catalog tracking all databases
WHERE datistemplate = false; -- datistemplate = false filters out the hidden system templates


-- psql meta command for listing tables: \dt
-- SQL Equivalent
SELECT table_name
FROM information_schema.tables -- information_schema is and ISO standard structure available in almost all Relational Databases (MySQL, SQL Server, Postgres)
WHERE table_schema = 'public';