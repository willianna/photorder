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
        # Samsung WB510 (SDC15036.jpg)
        match = re.search(r'SDC\d{5}', self.name, re.IGNORECASE)
        if match is not None:
            original_name = match[0].upper() + '.' + self.extension
            return 'Samsung WB510', original_name

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
                date = datetime.strptime(exif['datetime_original'], '%Y:%m:%d %H:%M:%S')

                # Samsung WB510 had wrong year settings after photo SDC14428
                if self.camera == 'Samsung WB510':
                    photo_id = re.search(r'SDC(\d{5})', self.name)
                    if int(photo_id.group(1)) > 14428:
                        if date.year == 2009:
                            date = date.replace(year=2011)
                        if date.year == 2010:
                            date = date.replace(year=2012)

                return date
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


    def restore_original_name(self):
        # Example of renaming: 2014-01-08_10-22-45_SAM_7074.jpg -> SAM_7074.jpg
        old_name = self.absolute_path
        print("       Old name:", old_name)
        if self.original_name is None:
            print("  ***SKIPPED***: original name is unknown\n")
            return False
        if self.name == self.original_name:
            print("  ***SKIPPED***: photo has original name already\n")
            return False

        new_name = os.path.join(self.directory, self.original_name)
        print("  Restored name:", new_name)

        if os.path.isfile(new_name):
            # TODO: should do here something about it
            print("  ***SKIPPED***: file exists")
            return False

        os.rename(old_name, new_name)
        return True


    def set_date_prefix(self):
        # Example of renaming: SAM_7074.jpg -> 2014-01-08_10-22-45_SAM_7074.jpg
        old_name = self.absolute_path
        print("  Old name:", self.absolute_path)
        if self.creation_date is None:
            print("  ***SKIPPED***: correct date is unknown\n")
            return False
        date_prefix = self.creation_date.strftime('%Y-%m-%d_%H-%M-%S_')
        if date_prefix in self.absolute_path:
            print("  ***SKIPPED***: correct date is already in the name\n")
            return False

        # trying to guess if there is SOME date prefix already
        match = re.search(r'\d{4}-\d{2}-\d{2}', self.name, re.IGNORECASE)
        if match is not None:
            return False
            # add here info about exceptions like wrong year for second camera
            print(f"  There is some date prefix already ({match[0]} instead of {date_prefix})")
            print(f"  Do you want to add correct one - {date_prefix + self.name}? (y/n) ", end='')
            answer = input()
            if answer != 'y':
                print("  ***SKIPPED***\n")
                return False

        new_name = os.path.join(self.directory, date_prefix + self.name)
        print("  New name:", new_name)

        if os.path.isfile(new_name):
            # TODO: should do here something about it
            print("  ***SKIPPED***: file exists")
            return False
            
        os.rename(old_name, new_name)
        return True


def is_photo(file):
    # Determine by extension if the file is photo (RAW or JPEG) or not
    extension = file.split('.')[-1]
    if extension in supported_raw_formats:
        return True
    if extension in supported_jpeg_formats:
        return True
    return False
