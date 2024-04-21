from functions import *

# setting up the database
setup_database()  # set to True if datatypes have already been created
populate_database()

# if the institution was not added yet, add it
print("\nCreating an institution:")
insert_institution("Museum2", "Paris, France")

# Borrow an artifact
print("\nBorrowing an artifact:")
# This function consists of 3 steps: it creates the entry for the artifact, creates the entry for the loan, creates the entry for transport of the artifact from institution to the museum
borrow_artifact("Portrait of Senior Bob", "It''s a painting of aforementioned Senior Bob", "Painting", "2 days", "Museum2", "2024-07-07")
# There are no special constraints other than proper formatting and the institution has to be existent

# Receive the borrowed artifact after being transported
print("\nReceiving the borrowed artifact:")
# This function consists of 3 steps: It ends the transport, creates an entry for inspection and changes the state of the artifact to being inspected
receive_artifact("Portrait of Senior Bob")

# After the inspection, cron job sets the status of the artifact to be available and is usable in the same way as owned artifacts

# Return the borrowed artifact
print("\nReturning the borrowed artifact:")
# This function consists of 2 steps: It sets the status of the artifact to in transit and creates an entry for the transport of the artifact
return_artifact_to_institution("Portrait of Senior Bob")

# Confirmation of return
print("\nThe institution confirming the return:")
# This function consists of 3 steps: It sets the status of the artifact to returned (meaning no longer in museum's possession)
# It ends the transport and ends the loan
artifact_reclaimed_by_institution("Portrait of Senior Bob")

# Examples of not-allowed actions
print("\nExamples of not-allowed actions:")
# Doing stuff with artifacts that aren't in the database
print("\nReceiving an artifact that wasn't borrowed:")
# Changing the status of an artifact will throw an error. The other two won't but they won't do anything
receive_artifact("Random painting")

# With artifacts that are in the database but are owned not borrowed, it won't throw an error, but it does nothing
# since WHERE clause only allows for artifacts that are in the borrowed ownership state
print("\nReturning an artifact that wasn't borrowed:")
return_artifact_to_institution("David")
