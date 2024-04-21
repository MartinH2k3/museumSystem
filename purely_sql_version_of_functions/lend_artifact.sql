-- The artifact cannot be used for exhibitions since it's loaned to some other institution at the time
UPDATE Artifacts SET status = 'loaned' WHERE LOWER(name) = LOWER(:artifact_name);
-- Creating a loan record for the artifact that is being lent to another institution
INSERT INTO Loans (artifact_id, institution_id, type, start_date) VALUES
    ((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name)),
    (SELECT id FROM Institutions WHERE LOWER(name) = LOWER(:borrowing_institution)), 'by museum', CURRENT_DATE);
