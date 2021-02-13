import os

def restore_names(photo_directory):
    pass

def rename_jpegs(photo_directory):
    print(f"Renaming all JPEGs in photo_directory: {len(photo_directory.photos)} photos")
    count = 0
    for photo in photo_directory.photos:
        # Example of renaming: SAM_7074.jpg -> 2014-01-08_10-22-45_SAM_7074.jpg
        date_prefix = photo.creation_date.strftime('%Y-%m-%d_%H-%M-%S_')
        new_name = os.path.join(photo.directory, date_prefix + photo.name)
        print("  Old name:", photo.absolute_path)
        print("  New name:", new_name)

        if date_prefix in photo.absolute_path:
            print("  ***SKIPPED***: correct date is already in the name\n")
        else:
            print()
            os.rename(photo.absolute_path, new_name)
            count += 1

    print(f"Done! Renamed {count} photos")

    pass