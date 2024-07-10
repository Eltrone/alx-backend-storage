-- Drop index if it already exists to avoid duplication errors
DROP INDEX IF EXISTS idx_name_first ON names;

-- Add a new column for storing the first letter of name
ALTER TABLE names ADD COLUMN first_letter CHAR(1) AS (LEFT(name, 1)) STORED;

-- Create an index on the newly created column
CREATE INDEX idx_name_first ON names(first_letter);
