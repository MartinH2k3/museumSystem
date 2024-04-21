INSERT INTO Exhibition_Artifacts (exhibition_id, artifact_id, exhibition_area_id) VALUES
(
    (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name)),
    (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER(:artifact_name) AND status = 'available'),
    (SELECT id FROM Exhibition_Areas WHERE exhibition_id =
        (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name))
        -- So input cannot be exhibition area used for different exhibition
    )
)