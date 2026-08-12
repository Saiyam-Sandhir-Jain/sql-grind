-- psql meta command for describing a table: \d [table_name]
-- SQL Equivalent
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_name = 'employees'
ORDER BY ordinal_position;

-- psql meta command for describe roles/users : \du
-- SQL Equivalent 1
SELECT 
    rolname AS "Role name",
    rolsuper AS "Superuser",
    rolcreaterole AS "Create role",
    rolcreatedb AS "Create DB",
    rolcanlogin AS "Cannot login (False) / Can login (True)"
FROM pg_roles;
