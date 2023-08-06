"""Emma
"""

from django.db.backends.signals import connection_created


def sqlite3_set_pragmas(sender, connection, **kwargs):
    """Set pragmas for SQLite connection."""
    cursor = connection.cursor()
    cursor.execute('PRAGMA synchronous = 1')
    cursor.execute('PRAGMA auto_vacuum = 1')
    cursor.execute('PRAGMA journal_mode = WAL')
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute(f'PRAGMA cache_size = {2 ** 13}')
    cursor.execute(f'PRAGMA mmap_size = {2 ** 26}')


connection_created.connect(sqlite3_set_pragmas)

__version__ = '0.0.1'
