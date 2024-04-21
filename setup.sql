DROP TABLE IF EXISTS inspections, transports, loans, exhibition_areas, exhibition_artifacts, areas, exhibitions, artifacts, institutions CASCADE;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    information TEXT
);

CREATE TABLE artifacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    status artifact_status NOT NULL,
    ownership ownership_status NOT NULL,
    inspection_duration INTERVAL NOT NULL
);

CREATE TABLE exhibitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    start_date TIMESTAMP NOT NULL CHECK (start_date >= CURRENT_DATE),
    end_date TIMESTAMP NOT NULL,
    status exhibition_status NOT NULL,
    CHECK (end_date >= start_date)
);

CREATE TABLE areas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE exhibition_areas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exhibition_id UUID REFERENCES exhibitions(id) NOT NULL,
    area_id UUID REFERENCES areas(id) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    CHECK (end_date >= start_date)
);

CREATE TABLE exhibition_artifacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    artifact_id UUID REFERENCES artifacts(id) NOT NULL,
    exhibition_id UUID REFERENCES exhibitions(id) NOT NULL,
    exhibition_area_id UUID REFERENCES exhibition_areas (id) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    CHECK (end_date >= start_date)
);

CREATE TABLE loans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    artifact_id UUID REFERENCES artifacts(id) NOT NULL,
    institution_id UUID REFERENCES institutions(id) NOT NULL,
    type transaction_direction NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP
);

CREATE TABLE transports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    artifact_id UUID REFERENCES artifacts(id) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP
);

CREATE TABLE inspections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    artifact_id UUID REFERENCES artifacts(id) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    CHECK (end_date >= start_date)
);

-- Create function to set and validate dates
CREATE OR REPLACE FUNCTION set_and_validate_dates()
RETURNS TRIGGER AS $$
DECLARE
    exhibition_record RECORD;
    artifact_status artifact_status;
BEGIN
    -- Get the exhibition dates
    SELECT start_date, end_date INTO exhibition_record
    FROM exhibitions WHERE id = NEW.exhibition_id;

    NEW.start_date := exhibition_record.start_date;
    NEW.end_date := exhibition_record.end_date;

    -- Validate that there is no overlap for Exhibition_Artifacts
    IF TG_TABLE_NAME = 'exhibition_artifacts' THEN
        SELECT status INTO artifact_status
        FROM artifacts WHERE id = NEW.artifact_id;

        IF artifact_status != 'available' THEN
            RAISE EXCEPTION 'Artifact is not in storage and cannot be part of an exhibition.';
        END IF;

        IF (SELECT COUNT(*) FROM exhibition_artifacts
            WHERE artifact_id = NEW.artifact_id AND
                  tsrange(NEW.start_date, NEW.end_date, '[]') &&
                  tsrange(start_date, end_date, '[]') AND
                  id != NEW.id -- Exclude the current record if updating
           ) > 0 THEN
           RAISE EXCEPTION 'Overlapping exhibition period for artifact.';
        END IF;
    END IF;

    -- Validate that there is no overlap for Exhibition_Areas
    IF TG_TABLE_NAME = 'exhibition_areas' THEN
        IF (SELECT COUNT(*) FROM exhibition_areas
            WHERE area_id = NEW.area_id AND
                  tsrange(NEW.start_date, NEW.end_date, '[]') &&
                  tsrange(start_date, end_date, '[]') AND
                  id != NEW.id -- Exclude the current record if updating
           ) > 0 THEN
           RAISE EXCEPTION 'Overlapping exhibition period for area.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_artifact_status_before_loan() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'loaned' AND OLD.status != 'available' THEN
        RAISE EXCEPTION 'Cannot loan artifact % as it is not in storage.', OLD.name;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers to apply the function
CREATE TRIGGER trigger_set_and_validate_exhibition_artifact_dates
BEFORE INSERT OR UPDATE ON exhibition_artifacts
FOR EACH ROW EXECUTE FUNCTION set_and_validate_dates();

CREATE TRIGGER trigger_set_and_validate_exhibition_area_dates
BEFORE INSERT OR UPDATE ON exhibition_areas
FOR EACH ROW EXECUTE FUNCTION set_and_validate_dates();

CREATE TRIGGER trigger_check_artifact_status_before_loan
BEFORE UPDATE ON artifacts
FOR EACH ROW EXECUTE FUNCTION check_artifact_status_before_loan();


