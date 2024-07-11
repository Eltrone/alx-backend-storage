-- Create the stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_weighted_score FLOAT;

    -- Calculate the total weighted score and the total weight
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_score, total_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the average weighted score
    SET average_weighted_score = total_score / total_weight;

    -- Update the average_score field in the users table
    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;
