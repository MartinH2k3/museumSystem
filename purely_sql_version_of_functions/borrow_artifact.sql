-- creates an entry for the borrowed artifact in the database. If it was borrowed before, it just updates to the newest information
INSERT INTO Artifacts (name, description, category, status, ownership, inspection_duration)
VALUES (:artifact_name, :description, :category, 'in transit', 'owned', :inspection_duration_interval) ON CONFLICT(name)
    DO UPDATE SET description = EXCLUDED.description, category = EXCLUDED.category, status = EXCLUDED.status, ownership = EXCLUDED.ownership, inspection_duration = EXCLUDED.inspection_duration;

-- creates an entry for the loan of the artifact, to track the loan history and where the artifact has been
INSERT INTO Loans (artifact_id, institution_id, type, start_date) VALUES
    ((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)),
    (SELECT id FROM Institutions WHERE LOWER(name) = LOWER(:owner_institution)), 'by museum', :start_date);

-- creates an entry for the transport of the artifact, to track when the artifact was being transported
INSERT INTO Transports (artifact_id, start_date) VALUES
    ((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)), CURRENT_DATE);