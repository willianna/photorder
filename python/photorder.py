import argparse

from lib import photo
from lib import tools


parser = argparse.ArgumentParser(description="Tool for photos reordering")
parser.add_argument(
    '-d', '--directory', dest='directory',
    help="directory with photos"
)
parser.add_argument(
    '-r', '--restore_names',
    action="store_true",
    help="restore original camera name"
)

args = parser.parse_args()


photo_directory = photo.PhotoDirectory(args.directory)

if (args.restore_names):
    tools.restore_names(photo_directory)

for photo in photo_directory.photos:
    photo.print_info()