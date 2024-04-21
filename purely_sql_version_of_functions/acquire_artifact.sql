INSERT INTO Artifacts (name, description, category, status, ownership, inspection_duration)
VALUES (:name, :description, :category, 'in storage', 'owned', :inspection_duration) ON CONFLICT(name)
    DO UPDATE SET description = EXCLUDED.description, category = EXCLUDED.category, status = EXCLUDED.status, ownership = EXCLUDED.ownership, inspection_duration = EXCLUDED.inspection_duration;"
