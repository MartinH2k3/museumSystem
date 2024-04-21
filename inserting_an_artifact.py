from functions import *

# setting up the database
setup_database() # set to True if datatypes have already been created
populate_database()

# This function is used when the museum buys a new artifact
print("\nCreating an artifact:")
acquire_artifact("Portrait of Senior Bob", "It''s a painting of aforementioned Senior Bob", "Painting", "2 days")

# In case the seller is not trustworthy or something along those lines, an inspection can be initiated
print("\nInspecting the artifact:")
begin_inspection("Portrait of Senior Bob")

# Duplicate insertion
print("\nDuplicate insertion:")
acquire_artifact("Portrait of Senior Bob", "It''s a painting of aforementioned Senior Bob", "Painting", "3 days")  # This will not create a new item, but rather it will update the existing one

# Example of not-allowed action
print("\nExample of not-allowed action:")
acquire_artifact("Portrait of Senior Bob", "It''s a painting of aforementioned Senior Bob", "Painting", "Bob")  # This will not work because the duration is not a proper interval
