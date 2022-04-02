import os
import re

def restore_names(photo_directory):
    print(f"Restoring original names in {photo_directory.path}: {len(photo_directory.photos)} photos")
    count = 0
    for photo in photo_directory.photos:
        if photo.restore_original_name():
            count += 1
        print()

    # TODO: exceptions like SAM_2456-2
    print(f"Done! Renamed {count} photos")


def rename_jpegs(photo_directory):
    print(f"Renaming all JPEGs in photo_directory: {len(photo_directory.photos)} photos")
    count = 0
    for photo in photo_directory.photos:
        if photo.set_date_prefix():
            count += 1
        print()

    print(f"Done! Renamed {count} photos")
