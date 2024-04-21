UPDATE Artifacts SET status = 'in transit'
WHERE LOWER(name) = LOWER(:artifact_name);

INSERT INTO Transports (artifact_id, start_date) VALUES
(
    (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)),
    CURRENT_DATE
);