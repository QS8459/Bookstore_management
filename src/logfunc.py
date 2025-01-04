import logging
import sqlite3
import csv
from logging.handlers import RotatingFileHandler

LOG_CSV_FILE = "error_logs.csv"

LOG_DB_FILE = "error_logs.db"

logger = logging.getLogger("Library_Logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

csv_handler = RotatingFileHandler(LOG_CSV_FILE, maxBytes = 1024 * 1024, backupCount = 3)
csv_handler.setLevel(logging.DEBUG)
csv_handler.setFormatter(logging.Formatter("%(asctime)s.%(levelname)s,%(message)s"))

class SQLiteHandler(logging.Handler):
    def __init__(self, db_path):
        super().__init__()
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.connection:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS error_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                message TEXT
            )
            """)

    def emit(self, record):
            log_entry = self.format(record)
            timeStamp, level, message = log_entry.split(',',2)
            with self.connection:
                self.connection.execute(
                    "INSERT INTO error_logs (timestamp, level, message) VALUES ( ?, ?, ?)",
                    (timeStamp,level, message )
                )

    def close(self):
        self.connection.close()
        super().close()


sqlite_handler = SQLiteHandler(LOG_DB_FILE)
sqlite_handler.setLevel(logging.DEBUG)
sqlite_handler.setFormatter(logging.Formatter("%(asctime)s, %(levelname)s, %(message)s"))
logger.addHandler(console_handler)
logger.addHandler(sqlite_handler)
logger.addHandler(csv_handler)