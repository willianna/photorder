import pathlib
import os
import re

supported_jpeg_formats = ['jpg', 'JPG', 'jpeg', 'JPEG']
supported_raw_formats = []

# TODOL logging

class PhotoDirectory(object):
    def __init__(self, directory):
        self.photos = self._initialize_directory(directory)
        self.path = directory
        # No such directory?

    def _initialize_directory(self, directory):
        photos = []

        # get all photos from the directory
        for root, dirs, files in (os.walk(directory)):
            for filename in files:
                if is_photo(filename):
                    photo = Photo(filename)
                    photos.append(photo)
        return photos


class Photo(object):
    def __init__(self, filename):
        self.name = filename
        self.extension = self._get_extension()
        self.absolute_path = os.path.abspath(filename)
        self.camera, self.original_name = self._get_camera_info()
        self.format = self._get_format()
        self.creation_date = None
        pass

    def _get_camera_info(self):
        # Samsung NX210 (SAM_7074.jpg)
        match = re.search(r'SAM_\d{4}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Samsung NX210', original_name

        # Canon G9X (IMG_1102.jpg)
        match = re.search(r'IMG_\d{4}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Canon G9X',original_name

        # Sony RX100 IV (DSC01524.ARW)
        match = re.search(r'DSC\d{5}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Sony RX100 IV', original_name


    def _get_format(self):
        if self.extension in supported_jpeg_formats:
            return 'JPEG'
        if self.extension in supported_raw_formats:
            return 'RAW'

    def _get_extension(self):
        extension = self.name.split('.')[-1]
        return extension

    def print_info(self):
        print('Name:', self.name)
        print('Camera:', self.camera)
        print('  Absolute path:', self.absolute_path)
        print('  Original name:', self.original_name)
        print('  Extension:', self.extension)
        print('  Format:', self.format)
        print('  Creation date:', self.creation_date)
        print()


def is_photo(file):
    extension = file.split('.')[-1]
    if extension in supported_raw_formats:
        return True
    if extension in supported_jpeg_formats:
        return True
    return False
