-- Create the stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE done INT DEFAULT 0;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Calculate the total weighted score and the total weight for the current user
        UPDATE users
        SET average_score = (
            SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
            FROM corrections
            INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id
        )
        WHERE id = user_id;

    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
