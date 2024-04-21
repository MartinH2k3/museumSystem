UPDATE Exhibitions SET status = :status WHERE LOWER(name) = LOWER(:exhibition_name);
-- Changes status of exhibition. Used to set status to 'prepared' from 'in preparation' after being prepared.
-- Other statuses get handled by cronjob anyways.