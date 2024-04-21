from functions import *

# setting up the database
setup_database()  # set to True if datatypes have already been created
populate_database()

# initiate exhibitions
print("\n\nInitiating exhibitions:")
initiate_exhibition("Exhibition 1", "It''s a magical exhibition about the ancient Egypt", "2025-06-01", "2025-06-30")
initiate_exhibition("Exhibition 2", "It''s a magical exhibition about the ancient Greece", "2025-06-02", "2025-07-02")
# examples of not-allowed actions
print("\nExamples of not-allowed actions:")
# This will not work because Exhibition 1 is already initiated
initiate_exhibition("Exhibition 1", "It''s a magical exhibition about the ancient Egypt", "2025-06-01", "2025-06-30")
# This will not work because the date is in the past
initiate_exhibition("Exhibition 3", "It''s a magical exhibition about the ancient Rome", "2020-06-01", "2020-06-30")
# This will not work because the end date is before the start date
initiate_exhibition("Exhibition 3", "It''s a magical exhibition about the ancient Rome", "2025-06-01", "2025-05-30")

# pick areas for the exhibitions
print("\n\nPick areas for the exhibitions:")
show_areas()  # first we need to know what areas there are to choose from them, so display them
# Out of the displayed ones choose some for the exhibition
print("\nChoosing areas for Exhibition 1:")
pick_area_for_exhibition("Main Hall", "Exhibition 1")
pick_area_for_exhibition("Entrance Hall", "Exhibition 1")
pick_area_for_exhibition("South Wing", "Exhibition 1")
print("\nChoosing areas for Exhibition 2:")
pick_area_for_exhibition("Room 1", "Exhibition 2")
pick_area_for_exhibition("Room 2", "Exhibition 2")
pick_area_for_exhibition("Room 3", "Exhibition 2")

# An example of not-allowed action
print("\nAn example of not-allowed action:")
pick_area_for_exhibition("Main Hall", "Exhibition 2")  # this will not work because the Main Hall is already taken

# pick artifacts for the exhibitions
print("\n\nInitiating exhibitions:")
show_artifacts()  # first we need to know what artifacts there are to choose from them, so display them

# Out of the displayed ones choose some for the exhibition
print("\nChoosing artifacts for Exhibition 1:")
pick_artifact_for_exhibition("Star of India", "Exhibition 1", "Main Hall")
pick_artifact_for_exhibition("The Orlov Diamond", "Exhibition 1", "Main Hall")
pick_artifact_for_exhibition("The Hope Diamond", "Exhibition 1", "Entrance Hall")
pick_artifact_for_exhibition("The Regent Diamond", "Exhibition 1", "Entrance Hall")
pick_artifact_for_exhibition("The Koh-i-Noor Diamond", "Exhibition 1", "South Wing")
pick_artifact_for_exhibition("The Sancy Diamond", "Exhibition 1", "South Wing")
print("\nChoosing artifacts for Exhibition 2:")
pick_artifact_for_exhibition("The Mona Lisa", "Exhibition 2", "Room 1")
pick_artifact_for_exhibition("The Birth of Venus", "Exhibition 2", "Room 1")
pick_artifact_for_exhibition("The Last Supper", "Exhibition 2", "Room 2")
pick_artifact_for_exhibition("The Creation of Adam", "Exhibition 2", "Room 2")
pick_artifact_for_exhibition("The Scream", "Exhibition 2", "Room 3")
pick_artifact_for_exhibition("The Pieta", "Exhibition 2", "Room 3")

# Examples of not-allowed actions
print("\nExamples of not-allowed actions:")
# This will not work because the Mona Lisa is already taken
pick_artifact_for_exhibition("The Mona Lisa", "Exhibition 1", "Main Hall")
# This will not work, because Room 12 isn't assigned to Exhibition 1
pick_artifact_for_exhibition("David", "Exhibition 1", "Room 12")

# move an artifact from one area to another
print("\n\nMoving an artifact from one area to another:")
move_artifact("The Hope Diamond", "Main Hall", "Exhibition 1")
# An example of not-allowed action
# This will not work because The Hope Diamond is not in the Exhibition 2
print("\nAn example of not-allowed action:")
move_artifact("The Hope Diamond", "Room 2", "Exhibition 2")
# This will not work because Room 2 is not assigned to Exhibition 1
move_artifact("The Hope Diamond", "Room 2", "Exhibition 1")

# set exhibition as prepared
print("\n\nSetting exhibitions as prepared:")
update_exhibition_status("Exhibition 1", "prepared")
# An example of not-allowed action
# This will not work because potato is not a valid status
print("\nAn example of not-allowed action:")
update_exhibition_status("Exhibition 1", "potato")

# change exhibition time
update_exhibition_times("Exhibition 1", "2025-06-15", "2025-07-15")
# Not-allowed actions same as in Exhibition initiation. Areas and Artifacts update will be success, but that's
# because the update on those doesn't work with the provided dates. It only matches the date to the exhibition dates.

