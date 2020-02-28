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
        if (!$timestamp) {
            print "It seems that $pic doesn't have EXIF info\n";
            next;
        }
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

    my @pics = grep {/\.(CR2|ARW|SRW)/} @all_files;
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

    if ($config->{'timestamp'}) {
        return $dir.'\\'.$config->{'timestamp'}.'_'.$pic;
    }
}

sub restore_original_name($$) {
    my $dir = shift;
    my @all_files = @{+shift};

    my @pics = grep {/\.(jpg|jpeg|JPG|JPEG)/} @all_files;

    # restoring JPEGs names, examples: SAM_7074.jpg, IMG_1102.jpg
    my $restored = 0;
    foreach my $pic (@pics) {
        my $full_name = $dir.'\\'.$pic;
        my $new_name;
        if ($pic =~ /((sam|img|SAM|IMG)_\d\d\d\d)/) {
            # photos from cameras: 20160208-sam_7074_32246700620_o.jpg, 20160512-SAM_4450.jpg
            $new_name = $dir.'\\'.uc($1);
            if ($pic =~ /\.(jpg|JPG|jpeg|JPEG)/) {
                $new_name = $new_name.".$1";
            }
        } elsif ($pic =~ /(\d\d\d\d-\d\d-\d\d)-(\d\d)(\d\d)(\d\d)\S+(\.\S+)/) {
            # photos from ipad/iphone: 2016-01-30-224544_28731621530_o.jpg
            $new_name = $dir.'\\'.$1." $2.$3.$4".$5;
        } else {
            next;
        }
        next if $full_name eq $new_name;

        print "$full_name to \n$new_name\n\n";
        if (-e $new_name) {
            print "Error: file $new_name exists\n";
            return 1;
        }
        if (!rename ($full_name, $new_name)) {
            print "Can't rename $pic: $!\n";
            return 1;
        }
        $restored++;
    }
    print "Restored names: $restored\n";
}

1;