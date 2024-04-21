UPDATE Exhibitions
    SET status = 'ongoing'
    WHERE start_date <= CURRENT_DATE AND end_date >= CURRENT_DATE AND status = 'prepared';

UPDATE Exhibitions SET status = 'finished' WHERE end_date < CURRENT_DATE;

UPDATE Artifacts SET status = 'in storage'
    WHERE status = 'being inspected' AND
        (SELECT end_date FROM Inspections WHERE artifact_id = id) < CURRENT_DATE;

-- Updates exhibition to 'ongoing' if it's start date is today or earlier (in case of sparse cronjob execution)
-- Updates exhibition to 'finished' if it's end date is today or earlier
-- Updates artifact to 'in storage' if it's inspection end date is today or earlier