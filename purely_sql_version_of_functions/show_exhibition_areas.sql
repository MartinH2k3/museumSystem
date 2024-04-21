SELECT * FROM Exhibition_Areas
WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name));
-- Shows all exhibition areas for specific exhibition