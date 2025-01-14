SELECT
    isotime AS "time",      -- Time column for X-axis
    temperature AS "value"  -- Value column for Y-axis
FROM
    tempdata
ORDER BY
    isotime ASC;