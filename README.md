Run `cuc.py` from your `.bashrc` to check for updating at most once a day whenever you open Cygwin.

    usage: cuc.py [-h] [-v] [-q] [-f] [--mirror HOST]
                  [--include PKGS | --exclude PKGS] [--cache-dir DIR]
                  [--setup-dir DIR]

    optional arguments:
      -h, --help       show this help message and exit
      -v               increase logging output to stderr (default: 0)
      -q               refrain from printing package list to stdout (default: False)
      -f               download from mirror even if setup.ini is in cache (default: False)
      --mirror HOST    cygwin mirror to download setup.ini from. (default: last mirror)
      --include PKGS   comma-separated list of packages to only consider (default: None)
      --exclude PKGS   comma-separated list of packages to not consider (default: None)
      --cache-dir DIR  directory to store cached files (default: /var/cache/setup)
      --setup-dir DIR  directory in which setup stores its files (default: /etc/setup)
