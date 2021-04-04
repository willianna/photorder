import os

def restore_names(photo_directory):
    print(f"Restoring original names in {photo_directory.path}: {len(photo_directory.photos)} photos")
    count = 0
    for photo in photo_directory.photos:
        # Example of renaming: 2014-01-08_10-22-45_SAM_7074.jpg -> SAM_7074.jpg
        print("       Old name:", photo.absolute_path)
        if photo.original_name is None:
            print("  ***SKIPPED***: original name is unknown\n")
            continue
        if photo.name == photo.original_name:
            print("  ***SKIPPED***: photo has original name already\n")
            continue

        new_name = os.path.join(photo.directory, photo.original_name)
        print("  Restored name:", new_name)

        os.rename(photo.absolute_path, new_name)
        count += 1
        print()

    # TODO: exceptions like SAM_2456-2
    print(f"Done! Renamed {count} photos")


def rename_jpegs(photo_directory):
    print(f"Renaming all JPEGs in photo_directory: {len(photo_directory.photos)} photos")
    count = 0
    for photo in photo_directory.photos:
        # Example of renaming: SAM_7074.jpg -> 2014-01-08_10-22-45_SAM_7074.jpg
        print("  Old name:", photo.absolute_path)
        if photo.creation_date is None:
            print("  ***SKIPPED***: correct date is unknown\n")
            continue
        date_prefix = photo.creation_date.strftime('%Y-%m-%d_%H-%M-%S_')
        if date_prefix in photo.absolute_path:
            print("  ***SKIPPED***: correct date is already in the name\n")
            continue

        new_name = os.path.join(photo.directory, date_prefix + photo.name)
        print("  New name:", new_name)

        os.rename(photo.absolute_path, new_name)
        count += 1
        print()

    print(f"Done! Renamed {count} photos")
