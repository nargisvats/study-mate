# PyMySQL fallback on Windows when mysqlclient is unavailable
import os

if os.environ.get("USE_MYSQL", "false").lower() == "true":
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
