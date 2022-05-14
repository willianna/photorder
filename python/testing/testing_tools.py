import json
import os
import shutil


def photo_pool():
    with open("testing/photo_pool.json") as photo_pool:
        return json.load(photo_pool)


def get_test_photo(name):
    get_from = os.path.abspath("testing/photo_pool" + "/" + name)
    copy_to = os.path.abspath("testing/__in_testing" + "/" + name)
    shutil.copy(get_from, copy_to)
    print(f"  Got test photo: {copy_to}")
    return copy_to


def rename(photo_path, new_name):
    old_name = photo_path
    new_name = os.path.join(os.path.dirname(old_name), new_name)
    os.rename(old_name, new_name)
    print(f"  Manually renamed to: {new_name}")
    return new_name
