import os
import hashlib
import time
import logging

class FileCache(object):

  def __init__(self, directory, expiration=86400):
    self.directory = directory
    self.expiration = expiration

  def _path(self, key):
    return self.directory + "/" + hashlib.sha256(key).hexdigest()

  def get(self, key):
    """Returns a string associated with the key.

    Args:
      key: A string used to lookup a string.
    
    Returns:
      A string associated with the key. If the key does not exist or has
      expired, None is returned.

    """
    logging.info('Getting %s from cache', key)
    path = self._path(key)
    logging.debug('Reading value from %s', path)
    try:
      value = open(path, "rb")
      mtime = os.path.getmtime(path)
    except Exception:
      logging.warning('%s not found in cache', key)
      return None
    if time.time() > mtime + self.expiration:
      logging.warning('%s expired in cache', key)
      logging.debug('Deleting %s', path)
      try:
        os.remove(path)
      except Exception:
        logging.error('Failed to delete %s', path)
      return None
    logging.info('%s found in cache', key)
    return value.read()

  def set(self, key, value):
    """Create or update a key-value pair in the cache.

    Args:
      key: A string to be used to lookup the value.
      value: A string associated with the key.

    Returns:
      A boolean that is True if and only if the pair was successfully written
      to the cache.

    """
    logging.info('Updating %s in cache', key)
    path = self._path(key)
    logging.debug('Writing to %s', path)
    try:
      open(path, 'wb').write(value)
    except Exception, e:
      logging.error('Failed to update %s in cache', key)
      return False
    return True
