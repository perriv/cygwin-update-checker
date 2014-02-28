import tempfile
import subprocess
import logging


_CYGWIN_PUBKEY = (
    '\x99\x01\xa2\x04HR\xfao\x11\x04\x00\xb9n}\xe7\xdb!\xb4z\xa3e\xa6\x0f\xc3\xec9'
    '\x19]\x07\xc5P\x16M\xd4>,/\xf3l\\\xa2\x12B@7\x16\xc8\x93zp\xd8\x0c\xc1B\xcbsI'
    '\x88 \xdc\x8a\x12i\xac\xfd\xb1\xb3\x81\\\xdb\x93\x04rbx\x8f\xd5\xfd\xdd\xb0\x95'
    '\xe0;G\xbfm\xaa;U\xd6\x1aLk\xfdt\tg\x16&S\x11a{0N\t\x97~\xc1x\xab\xd2,\xc8\xb0h!'
    'G_\x9e\x8b\xa8\xbe\xbc\xbe&E\x8c\xbc\xc2\x93\x02+\x07\xfc_J\x91\xcb\x00\xa0\xd6]'
    '\x89k\xddO\xb13\xba\x8a\xd5T\x00&\x0c\xbc\xa3E\x08q\x03\xfd\x17\xa7Po\xa4a\x17!'
    '\xf5\x81\xee\x0f\x01\xbd/\x19!\x83\x04\x84gCH\x19H\x19,s\x18\x1d\x90\xe5q`Q\xa1^'
    '\xae=\xca\x9a\xda"\xac\xf2\xfb\xc0\x10\xd3\x1c\x19j\xa8\xf9\xfb\x91\xc9\xc1\x90'
    '\xeb\xec\xe5\x16}\xbd"\x81\xebs\x13\x0c3n\xd5\xa6\'\xd0\xf7Sy\x02\xa8\x120\xf3'
    '\x88\x16B\xac{eM\x15\r\xa3/\x8bu5\xf7Pk4of\x88\xf0\x91{\x98c\xd9\x01\xd7\xa8tcff'
    '{S\xed\xe5\x18\x02\xff\x02\xe1\x03\xfe%\x92\xdbk\xb3q%\xce@\x0ef\xda\xd3\xc2.'
    '\xed\x08\x99\xcdG\xcf\xf9U\x89\xd5w\xad\xcd\x10l\x80^O\xea\xad\xa9T\xa1\x03\xbe'
    '\x18\xd4\x1ferT\xbc*\x18"\x18\xa7\x1e\x1e\xef\xcd\xfa\x8cOiu\x80h\xb4\x16\xe4'
    '\x94-}\xddc\x98\xec\x9bE\\\xbb\xe7\xfb\\\xb9C\xa0K\xab\xc7[\xc3`+\xfe\xf5\x00'
    '\x01@0\xcf^\xe6I\x93\x9ei\x0cmSA\xbb\xc0\x15_\x14\xeb\x05\x9d\x08\x8ea\x07\x07\t'
    '\xb07\xf0,\xcc\xf17\xb4\x1aCygwin <cygwin@cygwin.com>\x88^\x04\x13\x11\x02\x00'
    '\x1e\x05\x02HR\xfao\x02\x1b\x03\x06\x0b\t\x08\x07\x03\x02\x03\x15\x02\x03\x03'
    '\x16\x02\x01\x02\x1e\x01\x02\x17\x80\x00\n\t\x10\xa9\xa2b\xffg`A\xbaw\x19\x00'
    '\xa0\xa6}\x04\xb6D\xe7%\xf4\x7f\x15h\xa9\x9d0\xe0\x7f\x96\x83Q/\x00\x9fN\xac_['
    '\xa2\xfa\x89\xf9u\xb8<(\x1f\xcb|\xdc\xf4c\x91\x15\x88F\x04\x10\x11\x02\x00\x06'
    '\x05\x02HR\xfe\xa8\x00\n\t\x10M\xd2\x82\xe5j8\x8c>a\xfe\x00\xa0\xc1\xbe\x00\xc8'
    '\xc6E\xf8<\xa1\x18:E\xeb\xc0\xf8\x1c(gG\xa3\x00\xa0\xea\xdb\x06\xd8\x1a\xa3\xdd'
    '\xc4\xa4\xa0\x84\x9e\xed\xfd\xc9\xe6\xff;\x7fO\xb9\x01\r\x04HR\xfap\x10\x04\x00'
    '\x8a\x9c\xc3K\xdc\xa9\xd4\xef\xba\xe9&\xea\x88\x91S\x19\x10\xfe:\xcf\xfb\x8c6'
    '\x14\xd2\x84+[\x18\x1b\x9f\x9co\x05k\x7fr\x12MJ\xdbM\x16\xd5\xdc\\\xf9\x9e\x97'
    '\x9f\xc1\xa2\xcd\x94\x85#U\x80\x81\x05b\xf8>\xe5-/\x87\x02\xaef\xef1v\x9bI\x87'
    '\xf3\xda\xa8?j\xaa\xb0\xf7\x13Z\xe0oF\t\xd1x\x8f\xd0\x08e\xa5|\xe9A\xc4\x94-pd'
    '\x01\xd3\xbc\xc1\x1d\x80{<zOdo\x9a\xc3\x0c(T\x83!>\x9dt;\x00\x03\x05\x03\xfe+^'
    '\xae\xac\xc1\x1f&\xffS\xbc\x9d\x18\r\x93\x00\xefj\xcd\xc3mC\x88v\x86(\x14\xfa'
    '\xcd\xed\xed\x8b\x06\xe6\x16\x140~;b\x14\x9f\xab@\x80xC\xc6\x9c\xce\xf6\xfc9\xf1'
    'NZ\xff=s\x9b\xad\xcb\x7f\xdc\x9b\x1c5xstj\x89\xed\xae\xda\x86\xde\xae=J)+g\x9fn'
    '\xca\x94a\xaf\x15\x8fdY\xefV*\x1f\x997\xdd?\xa2\xa5F\x05>>\xa1\xb9\x93\x8b\x05&T'
    '\x92\x14\xcb\x8b\xd2d8\xc2\xd1Z\x99\x1c\xbc]8\x88I\x04\x18\x11\x02\x00\t\x05\x02'
    'HR\xfap\x02\x1b\x0c\x00\n\t\x10\xa9\xa2b\xffg`A\xbaz\xe0\x00\x9e)hX)\x98J\x9e'
    '\x14,!\xda\xb8C\x1b\xa2\x93\xb6\x8cYp\x00\xa0\xb0\x96\xed\x05\xb1\xf7\x0e\xffo'
    '\x80\xad\xeb\x0c\xeb\xb8BK\x0cP\xfa'
) 


class Setup(object):

  def __init__(self, directory='/etc/setup'):
    self.directory = directory


  def resources(self):
    '''
    Reads setup.rc into a dictionary.

    Returns:
      A dictionary representing the information presented in
      setup.rc. All entries besides mirrors-lst are treated as having
      values spanning one line. The value of mirrors-lst is
      represented as a list of tuples that contain the root path of
      the mirror, the mirror's host, the mirror's continent, and the
      mirror's country. For example:

      {
        'last-cache' : 'D:\Cygwin'
        'mirrors-lst' : [
          ('http://mirrors.163.com/cygwin/', 'mirrors.163.com', 'Asia', 'China'),
          ('http://box-soft.com/', 'box-soft.com', 'United States', 'Illinois'),
          ('http://cygwin.mirror.constant.com/', 'cygwin.mirror.constant.com', 'United States', 'New Jersey'),
          ...
        ],
        'last-mirror' : 'ftp://mirrors.kernel.org/sourceware/cygwin/',
        ...
      }

    Raises:
      IOError: An error occurred reading from setup.rc.

    '''
    setup_dict = {}
    setup_rc_path = self.directory + '/setup.rc'
    logging.info('Reading setup resources from %s', setup_rc_path)
    setup_rc = open(setup_rc_path, 'rb')
    key = None
    in_value = False
    for line in setup_rc:
      line = line.rstrip('\n')
      if line[0] != '\t':
        key = line
        if key == 'mirrors-lst':
          setup_dict['mirrors-lst'] = []
        in_value = True
        continue
      line = line[1:]
      if key == 'mirrors-lst':
        mirror_entry = line.split(';')
        setup_dict['mirrors-lst'].append(mirror_entry)
        continue
      # Treat the other values as strings on one line.
      setup_dict[key] = line
      in_value = False
    logging.debug(setup_dict)
    return setup_dict


  def installed_packages(self):
    '''
    Reads installed.db to extract installed package versions.

    Returns:
      A dictionary mapping installed packages to their versions. For example:

      {
        '_autorebase': '000107-1',
        '_update-info-dir': '00262-1',
        'alternatives': '1.3.30c-10',
        'base-cygwin': '3.3-1',
        'base-files': '4.1-1',
        'bash': '4.1.11-2',
        'binutils': '2.23.52-5',
        ...
      }

    Raises:
      IOError: An error occurred reading from installed.db.

    '''
    installed = {}
    installed_db_path = self.directory + '/installed.db'
    logging.info('Reading installed versions from %s', installed_db_path)
    installed_db = open(installed_db_path, 'rb')
    try:
      # Ignore the first line.
      first_line = installed_db.readline().rstrip('\n')
      for line in installed_db:
        # The 0's are ignored.
        line = line.rstrip('\n')
        words = line.split(' ')
        package = words[0]
        archive = words[1]
        # Strip off <package>- prefix and .tar.bz2 suffix.
        version = archive[len(package)+1:-8]
        installed[package] = version
    except Exception:
      raise IOError('An error occurred reading from ' + installed_db_path)
    logging.debug(installed)
    return installed


def verify_signature(data, sig=None):
  '''
  Verifies Cygwin's signature for the data with their public key
  using GPG.

  Args:
    data: A string containing raw signed data. If sig is omitted, it
      should also include its signature.
    sig: An optional string containing Cygwin's signature of the
      data. If omitted, the signature will be assumed to be included
      with the signed data (i.e. not detached).
  
  Returns:
    A boolean that is True if and only if the signature is good.

  Raises:
    NotImplementedError: The signature is not provided.
  
  '''
  logging.info('Verifying Cygwin signature')
  if sig is None:
    raise NotImplementedError('Signature must be detached')
  temp_pubkey = tempfile.NamedTemporaryFile()
  logging.debug('Writing public key to %s', temp_pubkey.name)
  temp_pubkey.write(_CYGWIN_PUBKEY)
  temp_pubkey.flush()
  temp_data = tempfile.NamedTemporaryFile()
  logging.debug('Writing signed data to %s', temp_data.name)
  temp_data.write(data)
  temp_data.flush()
  temp_sig = tempfile.NamedTemporaryFile()
  logging.debug('Writing signature to %s', temp_data.name)
  temp_sig.write(sig)
  temp_sig.flush()
  # GPG accepts unarmored public keys as keyrings
  cmd = 'gpg --status-fd 2 --no-default-keyring --keyring %s --verify %s %s' % (temp_pubkey.name, temp_sig.name, temp_data.name)
  logging.debug('Executing command: %s', cmd)
  proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for line in proc.stderr:
    if line.startswith('[GNUPG:] GOODSIG'):
      return True
  return False
