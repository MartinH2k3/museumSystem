-- If start_date and end_date are NULL, old values are retained
UPDATE Exhibitions SET start_date = COALESCE(:start_date, start_date), end_date = COALESCE(:end_date, end_date) WHERE LOWER(name) = LOWER(:exhibition_name);
-- Times are updates with trigger functions to match the Exhibition, so this update is used just to trigger them
UPDATE Exhibition_Areas SET start_date=start_date WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name));
UPDATE Exhibition_Artifacts SET start_date=start_date WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER(:exhibition_name));