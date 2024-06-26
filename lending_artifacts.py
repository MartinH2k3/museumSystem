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
# Passing non-existent artifacts or institutions will cause an error
print("\nExample of an error due to constraints:")
# Can't lend an artifact, that isn't at the museum's disposal
lend_artifact("Star of India", "The Louvre")

# getting the artifact back
# This function consists of 3 steps: Ending the loan, setting the status of the artifact to "being inspected" and creating a new inspection entry
receive_lent_artifact("Star of India")
# Receiving an artifact that wasn't a part of a loan doesn't throw errors, but doesn't do anything
