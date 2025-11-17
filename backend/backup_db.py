import shutil
import datetime
import os

DATABASE_PATH = "./sql_app.db"
BACKUP_DIR = "./backups"

def backup_database():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"sql_app_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copyfile(DATABASE_PATH, backup_path)
        print(f"Database backup successful: {backup_path}")
    except Exception as e:
        print(f"Database backup failed: {e}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    backup_database()
