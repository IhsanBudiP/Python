import logging
import logging.handlers
import datetime
import os

def remove_old_files(directory, days=90):
    """Removes files older than a specified number of days in a directory."""

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address='/dev/log', facility=logging.handlers.SysLogHandler.LOG_LOCAL7)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    now = datetime.datetime.now()
    cutoff_date = now - datetime.timedelta(days=days)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        try:
            if os.path.isfile(filepath):
                file_stats = os.stat(filepath)
                #print(file_stats)
                mtime = datetime.datetime.fromtimestamp(file_stats.st_mtime)
                #print(mtime)

                if mtime < cutoff_date:
                    logger = logging.getLogger(__name__)
                    logger.info(f"Deleting old backup file: {filepath}")
                    os.remove(filepath)

        except OSError as e:
            logger.error(f"Error processing {filepath}: {e}")
        except Exception as e:
            logger.error(f"A general error occurred: {e}")
        finally:
            logger.removeHandler(handler)


if __name__ == "__main__":
    directory = "{directory_to_check}"
    remove_old_files(directory,0)