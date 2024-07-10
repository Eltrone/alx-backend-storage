-- Drop the index if it already exists to avoid duplication errors
DROP INDEX IF EXISTS idx_name_first_score ON names;

-- Create an index on the first letter of the name and score
CREATE INDEX idx_name_first_score ON names ((LEFT(name, 1)), score);
