use Image::EXIF;
use File::stat;
use Time::Piece;
use Getopt::Long;

Getopt::Long::Configure(qw( bundling permute no_getopt_compat pass_through no_ignore_case ));

my (
    $debug,
    $raw,
    $jpeg,
    $dir,
    $prefix,
    $postfix,
) = ();

my %GetOptionsHash = (
    'debug'   => \$debug,
    'raw'     => \$raw,
    'jpeg'    => \$jpeg,
    'dir=s'   => \$dir,
    'prefix'  => \$prefix,
    'postfix' => \$postfix,
);
GetOptions( %GetOptionsHash ) or die "Couldn't parse options\n";

my $debug = 1;

# if $dir is not defined use current directory
$dir = '.' if (!defined $dir);

my $handle;
if (not opendir($handle, $dir)) {
    print "Cannot open directory\n";
    exit 1;
}
my @all_files = readdir($handle);
close($handle);

if ($jpeg or $all) {
    # renaming JPEGs using EXIF data
    my @pics = grep {/\.(jpg|jpeg|JPG|JPEG)/} @all_files;
    my $renamed = 0;
    foreach my $pic (@pics) {
        if ($pic =~ /^\d+/) {
            print "It seems that $pic has a date prefix already\n" if $debug;
            next;
        }
        my $pic_path = $dir.'\\'.$pic;
        my $exif = Image::EXIF->new($pic_path);
        my $other_info = $exif->get_other_info();

        my $prefix = $other_info->{'Image Generated'};
        $prefix =~ s/:/-/g;
        $prefix =~ s/ /_/g;

        print $prefix.'_'.$pic, "\n" if $debug;
        if (!rename ($pic_path, $dir.'\\'.$prefix.'_'.$pic)) {
            print "Can't rename $pic: $!\n";
        }
        $renamed++;
    }
    print "Renamed JPEGs: $renamed\n";
}

if ($raw or $all) {
    # renaming RAW using file stats
    @pics = grep {/\.(CR2|ARW)/} @all_files;
    $renamed = 0;
    foreach my $pic (@pics) {
        my $pic_path = $dir.'\\'.$pic;
        if ($pic =~ /^\d+/) {
            print "It seems that $pic has a date prefix already\n" if $debug;
            next;
        }
        my $data = stat($pic_path);
        my $time = localtime($data->mtime);
        my $prefix = $time->strftime("%Y-%m-%d").'_'.$time->strftime("%H-%M-%S");
        if (!rename ($pic_path, $dir.'\\'.$prefix.'_'.$pic)) {
            print "Can't rename $pic: $!\n";
        }
        print $pic_path, " to ", $dir.'\\'.$prefix.'_'.$pic, "\n" if $debug;
        $renamed++;
    }
    print "Renamed RAWs: $renamed";
}

exit 0;

# todo: 
#   check if prefix with date is correct
#   --force (rename even if there are prefix)
#   --restore (try to restore original name from camera)
