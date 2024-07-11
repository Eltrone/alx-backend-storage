-- Drop the function if it exists
DROP FUNCTION IF EXISTS SafeDiv;

-- Recreate the function with DOUBLE as the return type
DELIMITER $$

DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    RETURN IF(b = 0, 0, a / b);
END //
DELIMITER ;
