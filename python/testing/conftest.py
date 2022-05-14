import json
import os
import pytest
import os
import shutil
import pytest


@pytest.fixture(scope='session', autouse=True)
def testing_directory():
    directory = "testing/__in_testing"
    os.makedirs(directory, exist_ok=True)
    print(f"\n  Created directory: {os.path.abspath(directory)}")
    yield
    # remove directory after tests execution
    shutil.rmtree(directory)
    print(f"\n  Removed directory: {os.path.abspath(directory)}")
