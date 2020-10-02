import argparse
import pathlib
import os

# TODO: move to tools

supported_jpeg_formats = ['jpg', 'JPG', 'jpeg', 'JPEG']
supported_raw_formats = []

class PhotoDirectory(object):
    def __init__(self, directory):
        self.photos = self._initialize_directory(directory)
        self.path = directory

    def _initialize_directory(self, directory):
        photos = []

        # get all photos from the directory
        for root, dirs, files in (os.walk(directory)):
            for filename in files:
                photo = Photo(filename)
                photos.append(photo)
        return photos


class Photo(object):
    def __init__(self, filename):
        self.name = filename
        self.absolute_path = os.path.abspath(filename)
        self.camera_name = self._get_camera_name()
        self.extension = self._get_extension()
        self.format = self._get_format()
        self.creation_date = None
        pass

    def _get_camera_name(self):
        pass

    def _get_format(self):
        if self.extension in supported_jpeg_formats:
            return 'JPEG'
        if self.extension in supported_raw_formats:
            return 'RAW'

    def _get_extension(self):
        splitted_name = self.name.split('.')
        return splitted_name[-1]

    def print_info(self):
        print('Name: ', self.name)
        print('Absolute_path: ', self.absolute_path)
        print('Camera_name: ', self.camera_name)
        print('Extension: ', self.extension)
        print('Format: ', self.format)
        print('Creation_date: ', self.creation_date)
        print('\n')


def is_photo():
    # TODO
    pass


parser = argparse.ArgumentParser(description="Tool for photos reordering")
parser.add_argument(
    '-d', '--directory', dest='directory',
    help="directory with photos"
)
parser.add_argument(
    '-r', '--restore_name',
    action="store_true",
    help="restore original camera name"
)

args = parser.parse_args()

photo_directory = PhotoDirectory(args.directory)

for photo in photo_directory.photos:
    photo.print_info()