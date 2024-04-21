SELECT * FROM Exhibition_Artifacts
    WHERE exhibition_id =
        (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name));