import os
import re

from exif import Image
from datetime import datetime

supported_jpeg_formats = ['jpg', 'JPG', 'jpeg', 'JPEG']
supported_raw_formats = []

# TODO: logging

class PhotoDirectory(object):
    def __init__(self, directory):
        if not os.path.isdir(directory):
            # what type of exception is better to use here?
            raise Exception(f"Directory \"{directory}\" doesn't exist")
        self.path = directory
        self.photos = self._initialize_directory(directory)
        if not self.photos:
            raise Exception(f"Directory \"{directory}\" doesn't have photos")

    def _initialize_directory(self, directory):
        photos = []
        # get all photos from the directory
        for root, dirs, files in (os.walk(directory)):
            for filename in files:
                if is_photo(filename):
                    photo = Photo(os.path.abspath(directory + '/' + filename))
                    photos.append(photo)
            break # prevent descending into subfolders
        return photos


class Photo(object):
    def __init__(self, filename):
        self.name = os.path.basename(filename)
        self.extension = self._get_extension()
        self.absolute_path = filename
        self.directory = os.path.dirname(filename)
        self.camera, self.original_name = self._get_origin_info()
        self.format = self._get_format()
        self.creation_date = self._get_creation_date()
        pass

    def _get_origin_info(self):
        # Samsung NX210 (SAM_7074.jpg)
        match = re.search(r'SAM_\d{4}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Samsung NX210', original_name

        # Canon G9X (IMG_1102.jpg)
        match = re.search(r'IMG_\d{4}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Canon G9X', original_name

        # Sony RX100 IV (DSC01524.ARW)
        match = re.search(r'DSC\d{5}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Sony RX100 IV', original_name

        # exception
        return None, None


    def _get_format(self):
        if self.extension in supported_jpeg_formats:
            return 'JPEG'
        if self.extension in supported_raw_formats:
            return 'RAW'


    def _get_extension(self):
        extension = self.name.split('.')[-1]
        return extension


    def _get_creation_date(self):
        with open(self.absolute_path, 'rb') as photo:
            exif = Image(photo)
            if hasattr(exif, 'datetime_original'):
                return datetime.strptime(exif['datetime_original'], '%Y:%m:%d %H:%M:%S')
            else:
                return None


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
