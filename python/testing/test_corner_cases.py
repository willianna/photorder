import pytest
from lib.photo import Photo
import testing_tools


def test_photo_exists():
    # get the photo and rename to original name
    reference_photo_info = testing_tools.photo_pool()[-1]
    test_photo_path1 = testing_tools.get_test_photo(name=reference_photo_info['filename'],
                                                    new_name=reference_photo_info['original_name'])

    # get this exact photo again and rename to date_prefix_name
    reference_photo_info = testing_tools.photo_pool()[-1]
    test_photo_path2 = testing_tools.get_test_photo(name=reference_photo_info['filename'],
                                                    new_name=reference_photo_info['date_prefix_name'])

    test_photo = Photo(test_photo_path2)
    result = test_photo.restore_original_name()
    assert result == False, \
           f"Photo renaming should be skipped in this case"
