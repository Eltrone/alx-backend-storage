-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS before_email_update;

-- Change the delimiter to avoid issues with semicolons within the trigger body
DELIMITER $$

-- Create a new trigger
CREATE TRIGGER before_email_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END $$

-- Reset the delimiter back to semicolon
DELIMITER ;
