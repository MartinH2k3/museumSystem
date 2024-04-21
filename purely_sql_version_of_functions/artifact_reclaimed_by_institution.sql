=UPDATE Artifacts SET status = 'returned'
WHERE LOWER(name) = LOWER(:artifact_name);

UPDATE Loans SET end_date = CURRENT_DATE
WHERE artifact_id =
    (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)) AND end_date IS NULL;

UPDATE Transports SET end_date = CURRENT_DATE
WHERE artifact_id =
    (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)) AND end_date IS NULL;