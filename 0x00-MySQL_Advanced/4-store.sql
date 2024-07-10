-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS after_order_insert;

-- Change the delimiter to avoid issues with semicolons within the trigger body
DELIMITER $$

-- Create a new trigger
CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END $$

-- Reset the delimiter back to semicolon
DELIMITER ;
