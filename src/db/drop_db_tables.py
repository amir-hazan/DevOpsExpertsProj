import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import pymysql
from pypika import Column, Query
from src.App.AppSettings import ApplicationSettings


class DropDBTables:

    @staticmethod
    def drop_all_db_tables():
        """ Drop users & config table in db """

        get_db_tables_names = DropDBTables.check_if_tables_in_db()
        # print(type(get_db_tables_names))

        if len(get_db_tables_names) == 0:
            print("nothing to delete, number of table exist:", len(get_db_tables_names))
            return

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        for table_name in get_db_tables_names:
            # PyPika DROP
            drop_db_tables = Query.drop_table(table_name)
            drop_db_tables = drop_db_tables.get_sql()
            drop_db_tables = drop_db_tables.replace('"', '')
            cursor.execute(drop_db_tables)
            print("table:", table_name, "dropped successfully")

        try:
            conn.commit()
        except pymysql.err.OperationalError as pyExistErr:
            print("Error:", pyExistErr)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def check_if_tables_in_db():
        """ Check if users table exist in db """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        cursor, conn = get_app_settings_obj.connect_to_database()
        st_statement_to_execute = "SHOW TABLES"

        try:
            cursor.execute(st_statement_to_execute)
            db_table_list = []

            for table in [tables[0] for tables in cursor.fetchall()]:
                db_table_list.append(table)

            # print(db_table_list)

            if not db_table_list:
                return []

        except UnboundLocalError as localErr:
            print(localErr)
            return False

        finally:
            cursor.close()
            conn.close()

        return db_table_list


drop_tables_obj = DropDBTables
drop_tables_obj.drop_all_db_tables()
