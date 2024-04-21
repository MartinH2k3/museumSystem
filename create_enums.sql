CREATE TYPE artifact_status AS ENUM ('available', 'on display', 'loaned', 'returned', 'in transit', 'being inspected');
CREATE TYPE ownership_status AS ENUM ('owned', 'borrowed');
CREATE TYPE exhibition_status AS ENUM ('in preparation', 'prepared', 'ongoing', 'finished');
CREATE TYPE transaction_direction AS ENUM ('to museum', 'by museum');
