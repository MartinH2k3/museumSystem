INSERT INTO Inspections (artifact_id, start_date, end_date) VALUES
(
    (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)),
    CURRENT_DATE,
    CURRENT_DATE + (SELECT inspection_duration FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name))
);

UPDATE Artifacts SET status = 'being inspected' WHERE LOWER(name) = LOWER(:artifact_name);

UPDATE Loans SET end_date = CURRENT_DATE
WHERE artifact_id =
    (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)) AND end_date IS NULL;