use 5.6.0;

use strict;
use warnings;

use Getopt::Long;

use lib qw(.);
use tools;

Getopt::Long::Configure(qw( bundling permute no_getopt_compat pass_through no_ignore_case ));

my (
    $debug,
    $raw,
    $jpeg,
    $all,
    $dir,
) = ();

my %GetOptionsHash = (
    'debug'        => \$debug,
    'raw'          => \$raw,
    'jpeg'         => \$jpeg,
    'all'          => \$all,
    'dir=s'        => \$dir,
);
GetOptions( %GetOptionsHash ) or die "Couldn't parse options\n";

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
    if (tools::rename_jpeg($dir, \@all_files)) {
        exit 1;
    }
}

if ($raw or $all) {
    if (tools::rename_raw($dir, \@all_files)) {
        exit 1;
    }
}

exit 0;