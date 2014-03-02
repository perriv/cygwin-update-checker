#!/usr/bin/env python

import argparse
import logging
import os
import urllib2
import bz2

import cygwin
import cache


def parse_current_packages(ini):
  logging.info('Reading current versions from setup.ini')
  current = {}
  curr_pkg = None
  curr_grp = 'curr'
  in_val = False
  for line in ini.split('\n'):
    if len(line) == 0:
      continue
    # Override all other beginning-of-line indicators if we are in a
    # multi-lined value.
    if in_val:
      if line.endswith('"'):
        # Reached last line of value.
        in_val = False
      continue
    # Ignore comments.
    if line[0] == '#':
      continue
    # Package start.
    if line[0] == '@':
      curr_pkg = line[2:]
      curr_grp = 'curr'
      continue
    # Version group start. (Doesn't need to be specified for it to be curr.)
    if line[0] == '[':
      curr_grp = line[1:-1]
      continue
    # Current version statement. Keep it.
    if curr_grp == 'curr' and line.startswith('version: '):
      current[curr_pkg] = line[9:]
      continue
    # Detect a multi-lined value and override flow control if necessary.
    idx = line.find('"')
    if idx != -1 and line.find('"', idx + 1) == -1:
      in_val = True
      continue
    # Just skip over this single-lined value.
  logging.debug(current)
  return current


def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-v', dest='verbosity', action='count', default=0, help='increase logging output to stderr')
  parser.add_argument('-q', dest='quiet', action='store_true', help='refrain from printing package list to stdout')
  parser.add_argument('-f', dest='force_download', action='store_true', help='download from mirror even if setup.ini is in cache')
  parser.add_argument('--mirror', metavar='HOST', default='last mirror', help='cygwin mirror to download setup.ini from.')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--include', metavar='PKGS', help='comma-separated list of packages to only consider')
  group.add_argument('--exclude', metavar='PKGS', help='comma-separated list of packages to not consider')
  parser.add_argument('--cache-dir', metavar='DIR', default='/var/cache/setup', help='directory to store cached files')
  parser.add_argument('--setup-dir', metavar='DIR', default='/etc/setup', help='directory in which setup stores its files')
  args = parser.parse_args()

  # Logging configuration.
  try:
    severities = [logging.WARNING, logging.INFO, logging.DEBUG]
    min_severity = severities[args.verbosity]
  except IndexError:
    # A verbosity greater than 2 is treated as 2.
    min_severity = severities[2]
  logging.basicConfig(format='%(levelname)s: %(filename)s:%(lineno)d %(message)s', level=min_severity)

  # Create the cache if it doesn't exist.
  use_cache = not args.force_download
  if use_cache and not os.path.isdir(args.cache_dir):
    logging.info('Creating cache directory %s', args.cache_dir)
    try:
      os.makedirs(args.cache_dir)
    except IOError:
      logging.error('Failed to create cache directory')
      use_cache = False

  # Get information about the Cygwin setup.
  setup = cygwin.Setup(args.setup_dir)
  rc = setup.resources()
  installed = setup.installed_packages()
  mirror_root= None
  if args.mirror == 'last mirror':
    logging.info('Using last mirror')
    mirror_root = rc['last-mirror']
  else:
    logging.info('Selecting mirror root')
    mirror_roots = [d[0] for d in rc['mirrors-lst'] if d[1] == args.mirror]
    logging.debug(mirror_roots)
    try:
      mirror_root = mirror_roots[0]
    except IndexError:
      logging.error('%s not a Cygwin mirror', args.mirror)
      return

  # Download setup.ini from mirror.
  machine = os.uname()[4]
  if machine != 'x86_64':
    machine = 'x86'
  logging.debug('%s machine detected', machine)
  mirror_root = mirror_root + machine + '/'
  bz2_url = mirror_root + 'setup.bz2'
  ini = None
  if use_cache:
    fcache = cache.FileCache(args.cache_dir)
    ini = fcache.get(bz2_url)
  if ini is None:
    # File is not in cache, download and verify it.
    logging.warning('Downloading %s', bz2_url)
    ini_bz2 = urllib2.urlopen(bz2_url).read()
    ini = bz2.decompress(ini_bz2)
    sig_url = mirror_root + 'setup.ini.sig'
    logging.warning('Downloading %s', sig_url)
    ini_sig = urllib2.urlopen(sig_url).read()
    if cygwin.verify_signature(ini, ini_sig):
      logging.info('Verified setup.ini')
      if use_cache:
        fcache.set(bz2_url, ini)
    else:
      logging.warning('Could not verify downloaded setup.ini')
  current = parse_current_packages(ini)

  # Collect and filter out packages that have updates available.
  updates = []
  for pkg in installed.keys():
    installed_vers = installed[pkg]
    current_vers = current[pkg]
    if installed_vers != current_vers:
      updates.append((pkg, installed_vers, current_vers))
  if args.include is not None:
    include = args.include.split(',')
    updates = [p for p in updates if p[0] in include]
  if args.exclude is not None:
    exclude = args.exclude.split(',')
    updates = [p for p in updates if p[0] not in exclude]

  # Print out the available updates.
  if len(updates) == 0:
    return
  print '%d update%s available%s' % (len(updates), '' if len(updates) == 1 else 's', '' if args.quiet else ':')
  # Alignment
  max_1 = max([len(p[0]) for p in updates])
  max_2 = max([len(p[1]) for p in updates])
  max_3 = max([len(p[2]) for p in updates])
  form = '  %%%ds : %%%ds => %%%ds' % (max_1, max_2, max_3)
  if not args.quiet:
    for pkg_tuple in updates:
      print form % pkg_tuple

if __name__ == "__main__":
  main()
