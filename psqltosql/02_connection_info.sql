-- pgsql meta command to get infomation about the connection: \connectinfo
-- SQL Equivalent
SELECT 
    current_database() AS database,
    current_user AS user,
    inet_client_addr() AS client_ip,
    inet_server_port() AS port;
