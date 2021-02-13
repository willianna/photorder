import argparse

from lib import photo
from lib import tools


parser = argparse.ArgumentParser(description="Tool for photos reordering")
parser.add_argument(
    '-d', '--dir', dest='directory', # what if it is not set or doesn't exist?
    help="directory with photos"
)
parser.add_argument(
    '-r', '--restore_names',
    action="store_true",
    help="restore original camera name"
)
parser.add_argument(
    '-j', '--jpeg', dest='jpeg',
    action="store_true",
    help="rename all JPEGs in directory with date/time prefix"
)
parser.add_argument(
    '-i', '--info', dest='info',
    action="store_true",
    help="print info about all photos in the dorectory"
)

args = parser.parse_args()


photo_directory = photo.PhotoDirectory(args.directory)

if (args.restore_names):
    tools.restore_names(photo_directory)

if (args.jpeg):
    tools.rename_jpegs(photo_directory)

if (args.info):
    for photo in photo_directory.photos:
        photo.print_info()
        pass
