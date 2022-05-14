import pytest
from lib.photo import Photo
import testing_tools


@pytest.mark.parametrize("reference_photo_info", testing_tools.photo_pool())
def test_restore_original_name(reference_photo_info):
    test_photo_path = testing_tools.get_test_photo(reference_photo_info['filename'])
    test_photo_path = testing_tools.rename(test_photo_path, reference_photo_info['date_prefix_name'])

    test_photo = Photo(test_photo_path)
    print()
    print(f"       Original name according to tool: {test_photo.original_name}")
    print(f"  Original name according to reference: {reference_photo_info['original_name']}")
    assert test_photo.original_name == reference_photo_info['original_name'], \
           f"Tool reported wrong name {test_photo.original_name}"
