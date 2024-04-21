from db_facade import *


def setup_database(enums_exist=False):
    if not enums_exist:
        with open("create_enums.sql", "r") as file:
            query = file.read()
        print("Enums: " + insert_query(query))
    with open("setup.sql", "r") as file:
        query = file.read()
    print("Tables: " + insert_query(query))


def populate_database():
    with open("populate.sql", "r") as file:
        query = file.read()
    print("Populating: " + insert_query(query))


def insert_institution(name: str, information: str):
    query = f"INSERT INTO Institutions (name, information) VALUES ('{name}', '{information}') ON CONFLICT(name) DO UPDATE SET information = EXCLUDED.information;"
    print("Inserting institution into db: " + insert_query(query))


def cronjob():  # not sure entirely what this word means, but I hope it's right
    query = "UPDATE Exhibitions SET status = 'ongoing' WHERE start_date <= CURRENT_DATE AND end_date >= CURRENT_DATE AND status = 'prepared'; " \
             "UPDATE Exhibitions SET status = 'finished' WHERE end_date < CURRENT_DATE;"
    print("Periodic updating of exhibition statuses : " + insert_query(query))
    query = "UPDATE Artifacts SET status = 'available' WHERE status = 'being inspected' AND (SELECT end_date FROM Inspections WHERE artifact_id = id) < CURRENT_DATE;"
    print("Periodic updating of artifact inspection statuses : " + insert_query(query))


def show_artifacts(category=None):
    query = "SELECT * FROM artifacts" + (f" WHERE LOWER(category) = LOWER('{category}');" if category else ";")
    result = select_query(query)
    for artifact in result:
        print(artifact)


def initiate_exhibition(name: str, description: str, start_date: str, end_date: str):
    # Assuming dates are in correct format. Not checking here since postprocessing is forbidden.
    query = f"INSERT INTO Exhibitions (name, description, start_date, end_date, status) VALUES ('{name}', '{description}', '{start_date}', '{end_date}', 'in preparation');"
    print("Creating an entry for the exhibition: " + insert_query(query))


def update_exhibition_status(exhibition_name: str, status: str):
    query = f"UPDATE Exhibitions SET status = '{status}' WHERE LOWER(name) = LOWER('{exhibition_name}');"
    print("Updating exhibition status: " + insert_query(query))


def show_areas():
    query = "SELECT * FROM areas;"
    result = select_query(query)
    for area in result:
        print(area)


def pick_area_for_exhibition(area_name: str, exhibition_name: str):
    query = f"INSERT INTO Exhibition_Areas (exhibition_id, area_id) VALUES " \
                f"( (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}')), (SELECT id FROM Areas WHERE name = '{area_name}') );"
    print("Choosing area for an exhibition: " + insert_query(query))


def show_exhibition_areas(exhibition_name: str):
    query = f"SELECT * FROM Exhibition_Areas WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}'));"
    result = select_query(query)
    for area in result:
        print(area)


def pick_artifact_for_exhibition(artifact_name: str, exhibition_name: str, area_name: str):
    query = f"INSERT INTO Exhibition_Artifacts (exhibition_id, artifact_id, exhibition_area_id) VALUES " \
            f"((SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}')), " \
            f"(SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}') AND status = 'available'), " \
            f"(SELECT id FROM Exhibition_Areas WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}')) \
            AND area_id = (SELECT id FROM Areas WHERE LOWER(name) = LOWER('{area_name}'))));"
    print("Choosing artifact for an exhibition: " + insert_query(query))


def show_exhibition_artifacts(exhibition_name: str):
    query = f"SELECT * FROM Exhibition_Artifacts WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}'));"
    result = select_query(query)
    for artifact in result:
        print(artifact)


def update_exhibition_times(exhibition_name: str, start_date: str = None, end_date: str = None):
    start_date = "start_date" if not start_date else "'"+start_date+"'"
    end_date = "end_date" if not end_date else "'"+end_date+"'"

    query_exhibitions = f"UPDATE Exhibitions SET start_date = {start_date}, end_date = {end_date} WHERE LOWER(name) = LOWER('{exhibition_name}');"
    # These are automatically set to exhibition times after getting updated
    query_exhibition_areas = f"UPDATE Exhibition_Areas SET start_date=start_date WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}'));"
    query_exhibition_artifacts = f"UPDATE Exhibition_Artifacts SET start_date=start_date WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}'));"

    print("Exhibitions time update: " + insert_query(query_exhibitions))
    print("Exhibition Areas time update: " + insert_query(query_exhibition_areas))
    print("Exhibition Artifacts time update: " + insert_query(query_exhibition_artifacts))


def show_exhibitions():
    query = "SELECT * FROM Exhibitions;"
    result = select_query(query)
    for exhibition in result:
        print(exhibition)


# changes exhibition_area_id for exhibition_artefact
def move_artifact(artifact_name: str, area_name: str, exhibition_name: str):
    # This condition doesn't change anything, the second query wouldn't change anything, but this way, it doesn't say
    # that the query was a success if no items were updated
    check_query = f"SELECT * FROM Exhibition_Artifacts WHERE artifact_id = (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')) AND exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}'));"
    if not len(select_query(check_query)):
        print("Artifact not found in the exhibition")
        return
    query = f"UPDATE Exhibition_Artifacts SET exhibition_area_id = (SELECT id FROM Exhibition_Areas \
    WHERE exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}') AND\
    area_id = (SELECT id FROM Areas WHERE LOWER(name) = LOWER('{area_name}'))))\
    WHERE artifact_id = (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')) \
    AND exhibition_id = (SELECT id FROM Exhibitions WHERE LOWER(name) = LOWER('{exhibition_name}'));"
    print("Moving artifact between zones: " + insert_query(query))


# In java, this would be a private function
def insert_artifact(name: str, description: str, category: str, status: str, ownership: str, inspection_duration_interval: str):
    query = f"INSERT INTO Artifacts (name, description, category, status, ownership, inspection_duration) VALUES ('{name}', '{description}', '{category}', '{status}', '{ownership}', '{inspection_duration_interval}') ON CONFLICT(name)\
    DO UPDATE SET description = EXCLUDED.description, category = EXCLUDED.category, status = EXCLUDED.status, ownership = EXCLUDED.ownership, inspection_duration = EXCLUDED.inspection_duration;"
    return query


def acquire_artifact(name: str, description: str, category: str, inspection_duration_interval: str):
    query = insert_artifact(name, description, category, "available", "owned", inspection_duration_interval)
    print("Inserting artifact into db: " + insert_query(query))


# borrowing and lending artifacts

def start_transport(artifact_name: str):
    query = f"INSERT INTO Transports (artifact_id, start_date) VALUES ((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')), CURRENT_DATE);"
    print("Creating entry for transport: " + insert_query(query))


def end_transport(artifact_name: str):
    query = f"UPDATE Transports SET end_date = CURRENT_DATE WHERE artifact_id = (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')) AND end_date IS NULL;"
    print("Ending transport: " + insert_query(query))


def begin_inspection(artifact_name: str):
    query = f"INSERT INTO Inspections (artifact_id, start_date, end_date) VALUES ((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')), CURRENT_DATE, CURRENT_DATE + (SELECT inspection_duration FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')));"
    print("Creating entry for inspection: " + insert_query(query))
    query = f"UPDATE Artifacts SET status = 'being inspected' WHERE LOWER(name) = LOWER('{artifact_name}');"
    print("Artifact status update: " + insert_query(query))


def end_loan(artifact_name: str):
    query = f"UPDATE Loans SET end_date = CURRENT_DATE WHERE artifact_id = (SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')) AND end_date IS NULL;"
    print("Ending loan: " + insert_query(query))


# assumes parameters are correct
def borrow_artifact(name: str, description: str, category: str, inspection_duration_interval: str, owner_institution: str, start_date: str):
    insert_artifact_query = insert_artifact(name, description, category, "in transit", "borrowed", inspection_duration_interval)
    print("Inserting artifact into db: " + insert_query(insert_artifact_query))
    insert_loan_query = f"INSERT INTO Loans (artifact_id, institution_id, type, start_date) VALUES " \
                        f"((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{name}')), " \
                        f"(SELECT id FROM Institutions WHERE LOWER(name) = LOWER('{owner_institution}')), 'by museum', '{start_date}');"
    print("Inserting loan into db: " + insert_query(insert_loan_query))
    start_transport(name)


def receive_artifact(artifact_name: str):
    end_transport(artifact_name)
    begin_inspection(artifact_name)


def return_artifact_to_institution(artifact_name: str):
    query = f"UPDATE Artifacts SET status = 'in transit' WHERE LOWER(name) = LOWER('{artifact_name}') AND ownership='borrowed';"
    print("Artifact status update: " + insert_query(query))
    start_transport(artifact_name)


def artifact_reclaimed_by_institution(artifact_name: str):
    query = f"UPDATE Artifacts SET status = 'returned' WHERE LOWER(name) = LOWER('{artifact_name}') AND ownership='borrowed';"
    print("Artifact status update: " + insert_query(query))
    end_loan(artifact_name)
    end_transport(artifact_name)


def lend_artifact(artifact_name: str, borrowing_institution: str):
    query = f"UPDATE Artifacts SET status = 'loaned' WHERE LOWER(name) = LOWER('{artifact_name}') AND status = 'available';"
    print("Artifact status update: " + insert_query(query))
    query = f"INSERT INTO Loans (artifact_id, institution_id, type, start_date) VALUES " \
            f"((SELECT id FROM Artifacts WHERE LOWER(name) = LOWER('{artifact_name}')), " \
            f"(SELECT id FROM Institutions WHERE LOWER(name) = LOWER('{borrowing_institution}')), 'by museum', CURRENT_DATE);"
    print("Creating entry for loan: " + insert_query(query))


def receive_lent_artifact(artifact_name: str):
    print("Creating entry for inspection: " + insert_query(query))
    end_loan(artifact_name)
    begin_inspection(artifact_name)


# # setting up the exhibition
# initiate_exhibition("Exhibition 1", "First exhibition", "2024-06-05", "2024-06-30")
# initiate_exhibition("Exhibition 2", "Second exhibition", "2024-07-05", "2024-07-30")
# pick_area_for_exhibition("Main Hall", "Exhibition 1")
# pick_area_for_exhibition("East Wing", "Exhibition 1")
# pick_area_for_exhibition("West Wing", "Exhibition 1")
# pick_area_for_exhibition("South Wing", "Exhibition 2")
# pick_artifact_for_exhibition('Star of India', 'Exhibition 1', 'Main Hall')
# update_exhibition_status("Exhibition 1", "prepared")
# # cronjob()
# update_exhibition_times("Exhibition 1", start_date="2024-05-04")

#
# # moving artifact between zones
# move_artifact("Star of India", "East Wing", "Exhibition 1")
#
#
# # borrowing artifacts from other institutions
# # entry is created for the artifact, loan is created, transport is started
# borrow_artifact("Chinatown monkey", "A monkey statue from Beijing", "Statue", "1 month", "Alice Smith", "2024-06-05")
# # artifact is received, transport is ended, inspection is started
# receive_artifact("Chinatown monkey")
# # transport back is started
# return_artifact_to_institution("Chinatown monkey")
# # artifact is reclaimed by the institution, loan is ended, transport is ended
# artifact_reclaimed_by_institution("Chinatown monkey")
#
#
# # lending artifacts to other institutions, transport is started. Artifact is considered in transport the whole time it's loaned
# lend_artifact("Star of India", "The British Museum")
# # transport is ended, inspection is started
# receive_artifact("Star of India")