import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import pymysql
from pypika import Column, Query
from src.App.AppSettings import ApplicationSettings


class CreateDBTablesWithPrompt:

    @staticmethod
    def create_users_table():
        """ Creating users table in db """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        if CreateDBTablesWithPrompt.check_if_users_table_exist_in_db():
            print(get_app_settings_obj.get_users_db_table_name(), "table is already exist...")
        else:
            print("creating table:", get_app_settings_obj.get_users_db_table_name())

            # PyPika CREATE
            create_users_tbl = Query \
                .create_table(get_app_settings_obj.get_users_db_table_name()) \
                .columns(
                    Column(get_app_settings_obj.get_users_tbl_user_id_field(), "integer auto_increment", nullable=False),
                    Column(get_app_settings_obj.get_users_tbl_user_name_field(), "VARCHAR(50)", nullable=False),
                    Column(get_app_settings_obj.get_users_tbl_creation_date_field(), "DATETIME", nullable=False)) \
                .primary_key(get_app_settings_obj.get_users_tbl_user_id_field())

            create_users_tbl = create_users_tbl.get_sql()
            create_users_tbl = create_users_tbl.replace('"', '')

            try:
                cursor.execute(create_users_tbl)
                conn.commit()
                print("table:", get_app_settings_obj.get_users_db_table_name(), "created successfully\n")
            except pymysql.err.OperationalError as pyExistErr:
                print("Error:", pyExistErr)
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def create_config_table():
        """ Creating config table in db """
        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        if CreateDBTablesWithPrompt.check_if_config_table_exist_in_db():
            print(get_app_settings_obj.get_config_db_table_name(), "table is already exist...")
        else:
            print("creating table:", get_app_settings_obj.get_config_db_table_name())

            # PyPika CREATE
            create_config_tbl = Query \
                .create_table(get_app_settings_obj.get_config_db_table_name()) \
                .columns(
                    Column(get_app_settings_obj.get_config_db_id_field_name(), "integer auto_increment", nullable=False),
                    Column(get_app_settings_obj.get_config_db_protocol_field_name(), "VARCHAR(50)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_flask_host_field_name(), "VARCHAR(50)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_server_testing_host_field_name(), "VARCHAR(50)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_rest_app_port_field_name(), "integer", nullable=False),
                    Column(get_app_settings_obj.get_config_db_web_app_port_field_name(), "integer", nullable=False),
                    Column(get_app_settings_obj.get_config_db_users_endpoint_field_name(), "VARCHAR(55)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_get_user_data_endpoint_field_name(), "VARCHAR(55)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_create_users_endpoint_field_name(), "VARCHAR(55)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_get_all_users_endpoint_field_name(), "VARCHAR(55)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_stop_rest_server_endpoint_field_name(), "VARCHAR(55)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_stop_web_server_endpoint_field_name(), "VARCHAR(55)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_browser_field_name(), "VARCHAR(40)", nullable=False),
                    Column(get_app_settings_obj.get_config_db_user_name_field_name(), "VARCHAR(40)", nullable=False)) \
                .primary_key(get_app_settings_obj.get_config_db_id_field_name())

            create_config_tbl = create_config_tbl.get_sql()
            create_config_tbl = create_config_tbl.replace('"', '')

            try:
                cursor.execute(create_config_tbl)
                conn.commit()
                CreateDBTablesWithPrompt.insert_default_values_to_config_table()
                print("table:", get_app_settings_obj.get_config_db_table_name(), "created successfully\n")
            except pymysql.err.OperationalError as pyExistErr:
                print("Error:", pyExistErr)
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def check_if_users_table_exist_in_db():
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

            if get_app_settings_obj.get_users_db_table_name() in db_table_list:
                # print(get_users_db_table_name(), "table exist in list")
                users_table_index = db_table_list.index(get_app_settings_obj.get_users_db_table_name())
                # print("users table index:", users_table_index)
                return db_table_list[users_table_index]

            else:
                pass
                # print("not here")

        except UnboundLocalError as localErr:
            print(localErr)
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def check_if_config_table_exist_in_db():
        """ Check if config table exist in db """

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

            if get_app_settings_obj.get_config_db_table_name() in db_table_list:
                # print(get_config_db_table_name(), "table exist in list")
                config_table_index = db_table_list.index(get_app_settings_obj.get_config_db_table_name())
                # print("config table index:", config_table_index)
                return db_table_list[config_table_index]

            else:
                # print("not here")
                pass

        except UnboundLocalError as localErr:
            print(localErr)
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_default_values_to_config_table():
        """ Insert default values to config table """
        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika INSERT
        insert_into_confing_table = Query.into(get_app_settings_obj.get_db_schema_pypika_format().config) \
            .insert(
            get_app_settings_obj.set_config_db_table_field_id_value(),
            get_app_settings_obj.set_config_db_table_field_protocol_value(),
            get_app_settings_obj.set_config_db_table_field_host_value(),
            get_app_settings_obj.set_config_db_table_field_server_testing_host_value(),
            get_app_settings_obj.set_config_db_table_field_rest_app_port_value(),
            get_app_settings_obj.set_config_db_table_field_web_app_port_value(),
            get_app_settings_obj.set_config_db_table_field_users_endpoint_value(),
            get_app_settings_obj.set_config_db_table_field_get_users_data_endpoint_value(),
            get_app_settings_obj.set_config_db_table_field_create_users_endpoint_value(),
            get_app_settings_obj.set_config_db_table_field_get_all_users_endpoint_value(),
            get_app_settings_obj.set_config_db_table_field_stop_rest_server_value(),
            get_app_settings_obj.set_config_db_table_field_stop_web_server_value(),
            get_app_settings_obj.set_config_db_table_field_browser_value(),
            get_app_settings_obj.set_config_db_table_field_user_name_value()
        )

        insert_into_confing_table = insert_into_confing_table.get_sql()  # get Query as SQL
        insert_into_confing_table = insert_into_confing_table.replace('"', '')  # Removing apostrophes from relevant strings

        try:
            cursor.execute(insert_into_confing_table)
            conn.commit()
        except pymysql.err.OperationalError as pyExistErr:
            print("Error:", pyExistErr)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def run_create_tables():

        """ Verify tables creation """
        while True:
            try:
                user_input = int(input(
                    "### CREATE DB TABLES (users, config):\n"
                    "1. YES\n"
                    "2. NO, EXIT\n"
                    "### TYPE YOUR ANSWER: "
                ))

            except ValueError as valErr:
                # print("Error:", valErr, "\n\n")
                print("ANSWER MUST BE NUMBER, TRY AGAIN\n")
                continue

            if user_input not in range(1, 3):
                print("WRONG ANSWER, MUST BE BETWEEN 1 AND 2, TRY AGAIN!\n")

            else:
                if user_input == 1:
                    CreateDBTablesWithPrompt.create_users_table()
                    CreateDBTablesWithPrompt.create_config_table()
                    return
                elif user_input == 2:
                    print("exit from creating tables")
                    return


CreateDBTablesWithPrompt.run_create_tables()
