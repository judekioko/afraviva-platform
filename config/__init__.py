# PyMySQL is a pure-Python driver, unlike mysqlclient which needs a C compiler
# and MySQL dev headers — unavailable on Truehost's cPanel Python App build
# environment. Django's mysql backend imports MySQLdb though, so this shim
# makes PyMySQL answer to that name. Must run before anything imports the
# mysql backend, so it lives here rather than in settings.py.
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass  # not installed locally (SQLite dev doesn't need it)
