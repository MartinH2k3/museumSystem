INSERT INTO Exhibition_Areas (exhibition_id, area_id) VALUES
    (
        (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name)),
        (SELECT id FROM Areas WHERE name = :area_name)
    );
-- Adds area to exhibition