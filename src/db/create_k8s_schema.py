import os
import socket
import sys
import time
import pymysql
from pypika import Query, Column

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

from src.App.AppSettings import ApplicationSettings


class CreateK8SSchema:

    @staticmethod
    def wait_for_db(host, port):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                return True
            except socket.error:
                time.sleep(1)

    @staticmethod
    def connect_to_db_as_root():
        get_app_settings_obj = ApplicationSettings
        if CreateK8SSchema.wait_for_db(get_app_settings_obj.get_db_host(), get_app_settings_obj.get_db_port()) is True:
            db_connection_obj = ApplicationSettings
            """ Establish connection to MySQL DB """
            try:
                # Establishing connection to db as root user
                conn = pymysql.connect(
                    host=get_app_settings_obj.get_db_host(),
                    port=get_app_settings_obj.get_db_port(),
                    user="root",
                )
            except pymysql.err.OperationalError as operationalErr:
                print(operationalErr)
            finally:
                # Getting a cursor from Database
                cursor = conn.cursor()
                return cursor, conn

    @staticmethod
    def connect_to_db_as_admin():
        get_app_settings_obj = ApplicationSettings
        if CreateK8SSchema.wait_for_db(get_app_settings_obj.get_db_host(), get_app_settings_obj.get_db_port()) is True:
            """ Establish connection to MySQL DB """
            try:
                # Establishing connection to db as admin user
                conn = pymysql.Connect(
                    host=get_app_settings_obj.get_db_host(),
                    port=get_app_settings_obj.get_db_port(),
                    user=get_app_settings_obj.get_db_user_name(),
                    password=get_app_settings_obj.get_db_user_pass(),
                    db=get_app_settings_obj.get_db_schema_name()
                )
            except pymysql.err.OperationalError as operationalErr:
                print(operationalErr)
            finally:
                # Getting a cursor from Database
                cursor = conn.cursor()
                return cursor, conn

    @staticmethod
    def set_db_for_k8s():
        try:
            get_app_settings_obj = ApplicationSettings
            cursor, conn = CreateK8SSchema.connect_to_db_as_root()  # connect to database as root.

            show_db_query = 'SHOW DATABASES'
            cursor.execute(show_db_query)
            conn.commit()
            databases = [db[0] for db in cursor]

            # check if db exist
            devops_experts_db = get_app_settings_obj.get_db_schema_name()
            if devops_experts_db in databases:
                print(f"db '{devops_experts_db}' is exist")
            else:
                print("db is not exist, creating db...")
                create_db_query = f"CREATE DATABASE {devops_experts_db};"
                cursor.execute(create_db_query)
                # use DevOpsExpertsDB to work with.
                use_database_query = f"USE {devops_experts_db};"
                cursor.execute(use_database_query)

            # check if user admin is existed
            admin_user = get_app_settings_obj.get_db_user_name()
            admin_pass = get_app_settings_obj.get_db_user_pass()

            check_user_query = f"SELECT 1 FROM mysql.user WHERE user = '{admin_user}'"
            cursor.execute(check_user_query)
            user_exist = cursor.fetchone()

            if user_exist:
                print(f"The user {admin_user} already exists.")
            else:
                print(f"user '{admin_user}' is not exist, creating user {admin_user}")
                create_user_query = f"CREATE USER '{admin_user}'@'%' IDENTIFIED BY '{admin_pass}'"
                cursor.execute(create_user_query)

                # Grant privileges to the user
                grant_privileges_query = f"GRANT ALL PRIVILEGES ON {devops_experts_db}.* TO '{admin_user}'@'%'"
                cursor.execute(grant_privileges_query)
                print(f"Privileges have been granted to the user {admin_user} on database {devops_experts_db}.")

        except pymysql.err.OperationalError as e:
            print("1:", e)

        finally:
            # close connection for root user
            cursor.close()
            conn.close()

        try:
            # Establishing connection to db as admin user
            cursor, conn = CreateK8SSchema.connect_to_db_as_admin()  # connect to database as root.

            # start check and create users and config tables.
            check_users_table_exist = f"SELECT COUNT(*) FROM information_schema.tables " \
                                      f"WHERE table_schema = 'DevOpsExpertsDB' AND table_name = 'users'"

            cursor.execute(check_users_table_exist)

            is_users_table_exist = cursor.fetchone()[0]

            if is_users_table_exist:
                print("users table exist...")
            else:
                print("creating users table")
                create_users_tbl = Query \
                    .create_table(get_app_settings_obj.get_users_db_table_name()) \
                    .columns(
                        Column(get_app_settings_obj.get_users_tbl_user_id_field(), "integer auto_increment", nullable=False),
                        Column(get_app_settings_obj.get_users_tbl_user_name_field(), "VARCHAR(50)", nullable=False),
                        Column(get_app_settings_obj.get_users_tbl_creation_date_field(), "DATETIME", nullable=False)) \
                    .primary_key(get_app_settings_obj.get_users_tbl_user_id_field())

                create_users_tbl = create_users_tbl.get_sql()
                create_users_tbl = create_users_tbl.replace('"', '')
                cursor.execute(create_users_tbl)

            # check if config table exists
            check_config_table_exist = f"SELECT COUNT(*) FROM information_schema.tables " \
                                       f"WHERE table_schema = 'DevOpsExpertsDB' AND table_name = 'config'"

            cursor.execute(check_config_table_exist)

            is_config_table_exist = cursor.fetchone()[0]

            if is_config_table_exist:
                print("config table already exist.\nchecking if table is empty")

                check_config_table_is_empty = f"SELECT * FROM DevOpsExpertsDB.config;"
                cursor.execute(check_config_table_is_empty)

                config_rows = cursor.fetchall()
                if not config_rows:
                    print("table is empty, inserting data.")
                    insert_to_cnf_query = CreateK8SSchema.insert_values_to_config_table()
                    cursor.execute(insert_to_cnf_query)
                    conn.commit()

                else:
                    print("table is not empty.")

            else:
                print("creating config table.")

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

                cursor.execute(create_config_tbl)

                # insert default data to config table...
                print("inserting default data to config table...")

                insert_into_confing_table = CreateK8SSchema.insert_values_to_config_table()
                cursor.execute(insert_into_confing_table)
                conn.commit()

        except pymysql.err.OperationalError as pyExistErr:
            print("Error:", pyExistErr)
        finally:
            cursor.close()
            conn.close()

        return True

    @staticmethod
    def insert_values_to_config_table():
        # PyPika INSERT
        get_app_settings_obj = ApplicationSettings
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
        insert_into_confing_table = insert_into_confing_table.replace('"', '')

        return insert_into_confing_table


object_create_schema = CreateK8SSchema
object_create_schema.set_db_for_k8s()
