use 5.6.0;

use strict;
use warnings;

use Getopt::Long;

use lib qw(.);
use tools;
use utilities;

Getopt::Long::Configure(qw( bundling permute no_getopt_compat pass_through no_ignore_case ));

my (
    $debug,
    $raw,
    $jpeg,
    $restore,
    $all,
    $dir,
) = ();

my %GetOptionsHash = (
    'debug'        => \$debug,
    'raw'          => \$raw,
    'jpeg'         => \$jpeg,
    'restore'      => \$restore,
    'all'          => \$all,
    'dir=s'        => \$dir
);
GetOptions(%GetOptionsHash) or die "Couldn't parse options\n";

# if $dir is not defined use current directory
$dir = '.' if (!defined $dir);

if ($jpeg or $all) {
    if (tools::rename_jpeg($dir)) {
        exit 1;
    }
}

if ($raw or $all) {
    if (tools::rename_raw($dir)) {
        exit 1;
    }
}

if ($restore) {
    if (tools::restore_original_name($dir)) {
        exit 1;
    }
}

exit 0;
