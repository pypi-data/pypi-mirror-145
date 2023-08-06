# Calliope
# Copyright (C) 2018-2019  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import collections
import datetime
import json
import logging
import os
import pathlib
import sqlite3

import calliope.database

log = logging.getLogger(__name__)

'''cache: Simple key-value store for use by Calliope tools.

Many Calliope tools contact online services. We should always cache the
responses we get to avoid repeating the same request. This module provides a
simple key/value store interface that should be used for caching.

Use the `open()` module method to access a cache.

Multiple processes can read and write to a cache concurrently and can share data
appropriately.

'''


# Copied from pyxdg under the LGPL2 license. We avoid using the
# xdg.BaseDirectories module directly because we want to avoid using a globally
# cached xdg_cache_home directory, so we can run tests with
# click.testing.CliRunner and override XDG_CACHE_HOME in the environment.
def save_cache_path(*resource):
    """Ensure ``$XDG_CACHE_HOME/<resource>/`` exists, and return its path.
    'resource' should normally be the name of your application or a shared
    resource."""
    _home = os.path.expanduser('~')
    xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or \
                os.path.join(_home, '.cache')

    resource = os.path.join(*resource)
    assert not resource.startswith('/')
    path = os.path.join(xdg_cache_home, resource)
    if not os.path.isdir(path):
        os.makedirs(path)
    return pathlib.Path(path)


CacheLookupResult = collections.namedtuple(
    'CacheLookupResult',
    ['found_timestamp', 'value'])
"""The result of looking for a value in a cache.

If the value is found, ``found_timestamp`` will be set to the
datetime of when it was stored. Otherwise, ``found_timestamp`` will be ``None``.
"""


class Cache():
    '''Abstract base class that defines the Cache interface.

    Do not use this class directly. Call the `open()` module method instead.

    '''
    def __init__(self, namespace, cachedir=None):
        raise NotImplementedError("Use the cache.open() function to open a cache")

    def lookup(self, key) -> CacheLookupResult:
        '''Lookup 'key' in the cache.

        Returns a :class:`CacheLookupResult` tuple.

        '''
        raise NotImplementedError()

    def store(self, key, value, timestamp=None):
        '''Store 'value' in the cache under the given key.

        The contents of 'value' must be representable as JSON data.

        The value will be marked with the current timestamp so cache expiry
        can be done. The ``timestamp`` parameter overrides this if needed.

        '''
        raise NotImplementedError()

    def wrap(self, key, call, expiry: datetime.timedelta = None):
        '''Either run call() and save the result, or return cached result.

        This is intended for use when calling remote APIs. Lots of network access
        can be avoided if the result is saved for future use. For example, this
        snipped is used in the lastfm.similar_artists() function:

            def similar_artists(lastfm, artist_name):
                entry = lastfm.cache.wrap('artist-similar:{}'.format(artist_name),
                    lambda: lastfm.api.artist.get_similar(artist_name, limit=count))

        By default, items in the cache never expire. You can pass a
        `datetime.timedelta` instance to force entries to expire after a
        certain time period. This may be an hour, a day or a week depending
        how soon changes in the remote API result need to be detected.

        '''
        found_timestamp, entry = self.lookup(key)
        if found_timestamp:
            log.debug("Found {} in cache from {}".format(key, found_timestamp))
            if expiry is None:
                log.debug("  - cache expiry disabled")
                return entry
            else:
                now = datetime.datetime.now()
                valid_until_datetime = found_timestamp + expiry
                if valid_until_datetime >= now:
                    log.debug("  - value is valid until {}"
                              .format(valid_until_datetime.isoformat()))
                    return entry
                else:
                    log.debug("  - value expired on {}"
                              .format(valid_until_datetime.isoformat()))
        else:
            log.debug("Didn't find {} in cache".format(key))

        log.debug("Running remote query for {}".format(key))
        entry = call()
        self.store(key, entry)
        return entry


class SqliteCache(Cache):
    '''Cache implemention which uses the SQLite database library.'''

    # FIXME: this would be much faster if we could use sqlite3_stmt_prepare.
    # Seems that the sqlite3 module doesn't expose that though.

    def __init__(self, namespace, cachedir=None):  # pylint: disable=super-init-not-called
        if cachedir is None:
            cachedir = save_cache_path('calliope')

        self._path = os.path.join(cachedir, namespace) + '.sqlite'
        self.__connection = None

    def _get_schema_version(self):
        cursor = self.__connection.execute('PRAGMA user_version')
        # This should always succeed, so propagate exceptions as errors.
        row = cursor.fetchone()
        return int(row[0])

    def _set_schema_version(self, version):
        self.__connection.execute(f'PRAGMA user_version={version}')

    def _connection(self):
        if self.__connection:
            return self.__connection

        self.__connection = sqlite3.connect(self._path)
        # See: https://sqlite.org/wal.html
        self.__connection.execute('PRAGMA journal_mode=WAL;')

        if self._get_schema_version() == 0:
            log.debug("%s: Initializing to version 2", self._path)
            with self.__connection:
                self.__connection.execute(
                    'CREATE TABLE IF NOT EXISTS cache (key STRING UNIQUE, value, timestamp DATETIME);'
                )
                self._set_schema_version(2)
        elif self._get_schema_version() == 1:
            log.debug("%s: Updating to version 2", self._path)
            with self.__connection:
                self.__connection.execute('ALTER TABLE cache ADD COLUMN timestamp DATETIME')
                self._set_schema_version(2)

        return self.__connection

    def lookup(self, key):
        '''Lookup 'key' in the cache.

        Returns a tuple of (found_timestamp, value). If the value is not
        found in the cache, both values will be None.

        '''
        if not os.path.exists(self._path):
            return None, None
        db = self._connection()
        cursor = db.execute('SELECT value, timestamp FROM cache WHERE key=?', (key,))
        row = cursor.fetchone()
        if row:
            value = json.loads(row[0])
            if row[1] is None:
                log.debug("No timestamp, returning UNIX epoch.")
                timestamp = 0
            else:
                log.debug("Timestamp is %s", row[1])
                timestamp = datetime.datetime.fromisoformat(row[1])
            return (timestamp, value)
        else:
            return (None, None)

    def store(self, key, value, timestamp=None):
        timestamp = timestamp or datetime.datetime.now()

        db = self._connection()
        db.execute('INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?);',
                   (key, json.dumps(value), timestamp))
        calliope.database.sqlite3_commit_with_retry(db, max_retries=3)


def open(namespace, cachedir=None):  # pylint: disable=redefined-builtin
    '''Open a cache using the best available cache implementation.

    The 'namespace' parameter should usually correspond with the name of tool
    or module using the cache.

    The 'cachedir' parameter is mainly for use during automated tests.

    '''
    return SqliteCache(namespace, cachedir=cachedir)
