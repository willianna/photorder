package tools;

use strict;
use warnings;

use Image::EXIF;
use File::stat;
use Time::Piece;

sub rename_jpeg($$) {
    my $dir = shift;
    my @all_files = @{+shift};

    my @pics = grep {/\.(jpg|jpeg|JPG|JPEG)/} @all_files;

    # renaming JPEGs using EXIF data
    my $renamed = 0;
    foreach my $pic (@pics) {
        if ($pic =~ /^\d+/) {
            print "It seems that $pic has a date prefix already\n";
            next;
        }
        my $full_name = $dir.'\\'.$pic;
        my $exif = Image::EXIF->new($full_name);
        my $other_info = $exif->get_other_info();

        my $timestamp = $other_info->{'Image Generated'};
        $timestamp =~ s/:/-/g;
        $timestamp =~ s/ /_/g;

        my $new_name = compose_new_name($pic, $dir, {'timestamp' => $timestamp});
        print "$full_name to \n$new_name\n\n";
        if (!rename ($full_name, $new_name)) {
            print "Can't rename $pic: $!\n";
            return 1;
        }
        $renamed++;
    }
    print "Renamed JPEGs: $renamed\n";

    return 0;
}

sub rename_raw($$) {
    my $dir = shift;
    my @all_files = @{+shift};

    my @pics = grep {/\.(CR2|ARW)/} @all_files;
    my $renamed = 0;
    foreach my $pic (@pics) {
        my $full_name = $dir.'\\'.$pic;
        if ($pic =~ /^\d+/) {
            print "It seems that $pic has a date prefix already\n";
            next;
        }

        # renaming RAW using file stats
        my $data = stat($full_name);
        my $time = localtime($data->mtime);
        my $timestamp = $time->strftime("%Y-%m-%d").'_'.$time->strftime("%H-%M-%S");

        my $new_name = compose_new_name($pic, $dir, {'timestamp' => $timestamp});
        if (!rename ($full_name, $new_name)) {
            print "Can't rename $pic: $!\n";
        }
        print "$full_name to \n$new_name\n\n";
        $renamed++;
    }
    print "Renamed RAWs: $renamed";
}

sub compose_new_name($$$) {
    my $pic = shift;
    my $dir = shift;
    my $config = shift;

    return $dir.'\\'.$config->{'timestamp'}.'_'.$pic;
}

1;