import os
import sys
import time

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

from src.App.AppSettings import ApplicationSettings
from pypika import Column, Query
import pymysql


class CheckTableExist:

    @staticmethod
    def check_if_tables_exist():
        """ Check if tables exist in db """
        get_app_settings_obj = ApplicationSettings
        current_try, max_retry, retry_interval = 0, 5, 3
        is_table_exist = False

        while is_table_exist is False and current_try < max_retry:
            cursor, conn = get_app_settings_obj.connect_to_database()
            check_tables_statement_to_execute = "SHOW TABLES"

            try:
                cursor.execute(check_tables_statement_to_execute)
                db_tables_list = []

                if cursor.rowcount != 0:
                    # print("row count:", cursor.rowcount)

                    for table in [tables[0] for tables in cursor.fetchall()]:
                        db_tables_list.append(table)

                    # print(db_tables_list)

                    if get_app_settings_obj.get_users_db_table_name() not in db_tables_list or \
                            get_app_settings_obj.get_config_db_table_name() not in db_tables_list:

                        print("Only '" + str(*db_tables_list) + "' table was found in list attempts left",
                              max_retry - current_try, "trying again in:", retry_interval, "sec...")
                        current_try += 1
                        time.sleep(retry_interval)

                    else:
                        # print("both tables in list, continue script...")
                        is_table_exist = True

                else:
                    print("No tables found in db, retries left", max_retry - current_try, "trying again in:",
                          retry_interval, "sec...")
                    current_try += 1
                    time.sleep(retry_interval)

            except UnboundLocalError as localErr:
                print(localErr)
                return False

            finally:
                cursor.close()
                conn.close()

        if is_table_exist is True:
            return True
        else:
            return False
