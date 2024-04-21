from functions import *

# setting up the database
setup_database()  # set to True if datatypes have already been created
populate_database()

# if the institution was not added yet, add it
print("\nCreating an institution:")
insert_institution("Museum2", "Paris, France")

# Since when borrowing, both directions of the transportation were handled by the museum
# it's safe to assume the borrower always handles the transportation

# lending the artifact
# This function consists of 2 steps: Setting the status of the artifact to "loaned" and creating a new loan entry
lend_artifact("Star of India", "Museum2")
