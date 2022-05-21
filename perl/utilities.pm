package utilities;

my @raw_formats = ('CR2', 'ARW', 'SRW');
my @jpeg_formats = ('jpg', 'jpeg', 'JPG', 'JPEG');

sub get_files($$) {
    my $dir = shift;
    my $type = shift;

    my $handle;
    if (not opendir($handle, $dir)) {
        print "Cannot open directory\n";
        exit 1;
    }
    my @all_files = readdir($handle);
    close($handle);

    if ($type eq 'all') {
        return \@all_files;
    }

    my $regexp;
    if ($type eq 'jpeg') {
        $regexp = join("|", @jpeg_formats);
    } elsif ($type eq 'raw') {
        $regexp = join("|", @raw_formats);
    } else {
        print "SCRIPT ISSUE: Unknown type: $type\n";
        return ();
    }

    # grep here is like {/\.(CR2|ARW|SRW)/}
    my @pics = grep {/\.($regexp)/} @all_files;
    return \@pics;
}
