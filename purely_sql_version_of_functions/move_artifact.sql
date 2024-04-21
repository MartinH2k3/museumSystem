UPDATE Exhibition_Artifacts SET exhibition_area_id =
    (
    SELECT id FROM Exhibition_Areas
        WHERE exhibition_id =
            (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name)
        AND area_id =
            (SELECT id FROM Areas WHERE LOWER(name) = LOWER(:area_name)))
    )
    WHERE artifact_id =
        (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name))
    AND exhibition_id =
        (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name));

-- Moves artifacts between areas within the same exhibition