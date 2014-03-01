Run `cuc.py` from your `.bashrc` to check for updating at most once a day whenever you open Cygwin.

    usage: cuc.py [-h] [-v] [-q] [--mirror HOST] [--cache-dir DIR]
                  [--setup-dir DIR] [--force-download]
                  [--include PKGS | --exclude PKGS]
    
    optional arguments:
      -h, --help        show this help message and exit
      -v                increase logging output to stderr (default: 0)
      -q                do not print package list to stdout (default: False)
      --mirror HOST     cygwin mirror (default: last mirror)
      --cache-dir DIR   directory to store cached files (default:
                        /var/cache/setup)
      --setup-dir DIR   directory in which setup stores its files (default:
                        /etc/setup)
      --force-download  do not use cache (default: False)
      --include PKGS    comma-separated list of packages to only consider
                        (default: None)
      --exclude PKGS    comma-separated list of packages to not consider (default:
                        None)
