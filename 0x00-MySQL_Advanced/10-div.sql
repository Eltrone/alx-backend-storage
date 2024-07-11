DROP FUNCTION IF EXISTS SafeDiv;

DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS VARCHAR(64)
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN '0';
    ELSE
        -- Convert calculation result to string with high precision
        RETURN CAST(a / b AS DECIMAL(20,15));
    END IF;
END$$

DELIMITER ;
