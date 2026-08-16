WITH
    same_department AS (
        SELECT
            e.emp_id AS emp_a,
            d.emp_id AS emp_b
        FROM employees AS e
        JOIN employees d ON (e.dept_id = d.dept_id AND e.emp_id < d.emp_id)
    ),

    same_job_title AS (
        SELECT
            e.emp_id emp_a,
            j.emp_id emp_b
        FROM employees AS e 
        JOIN employees j ON (e.job_title = j.job_title AND e.emp_id < j.emp_id)
    )

SELECT
    sd.emp_a,
    sd.emp_b
FROM same_department AS sd 
WHERE EXISTS (
    SELECT 1
    FROM same_job_title AS sjt 
    WHERE (
        sd.emp_a = sjt.emp_a
        AND sd.emp_b = sjt.emp_b
    )
);
