import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import pymysql
import random
from src.App.AppSettings import ApplicationSettings
from pypika import Table, Query
import itertools
import json


class DBConnector:
    """ Class that handle all Queries and logic To / From DB """
    def __init__(self,
                 user_id,
                 user_name,
                 date_created,
                 new_user_name):

        self.user_id = user_id
        self.user_name = user_name
        self.date_created = date_created
        self.new_user_name = new_user_name

    def add_new_user(self):
        """ SQL Query for adding new user to users table """

        user_id = self.user_id
        user_name = self.user_name
        date_created = self.date_created

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika INSERT
        insert_user_query = Query.into(get_app_settings_obj.get_db_schema_pypika_format().users).insert(
            user_id,
            user_name,
            date_created
        )

        insert_user_query = insert_user_query.get_sql()  # get Query as SQL
        insert_user_query = insert_user_query.replace('"', '')  # Removing apostrophes from relevant strings

        try:
            cursor.execute(insert_user_query)
            conn.commit()
            # print(cursor.rowcount, "record inserted.")

        except pymysql.err.IntegrityError as sqlError:
            # Catch Exception if user exist or not
            print("Error:", sqlError)
            return False

        finally:
            # Close connection and cursor
            cursor.close()
            conn.close()

        return True

    def get_existing_user_by_id(self):
        """ SQL Query for getting username by user id from users table """

        user_id = self.user_id

        # check if user_id is alphanumeric, return user_name False if not
        if not user_id.isalnum():
            user_name = False
            date_created = False
            return user_name, date_created

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika SELECT
        users = Table(get_app_settings_obj.get_users_db_table_name())
        select_user_query = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select(
            users.user_id,
            users.user_name,
            users.creation_date
        ).where(
            users.user_id == user_id
        )

        select_user_query = select_user_query.get_sql()
        select_user_query = select_user_query.replace('"', '').replace("'", '')

        try:
            cursor.execute(select_user_query)
            conn.commit()

            users_list = []

            for row in cursor:
                users_list.append(row)

            user_name = row[1]
            date_created = row[2]

        except pymysql.err.OperationalError as err:
            user_name = False
            date_created = False
            return user_name, date_created

        except UnboundLocalError as localError:
            # print("Error:", localError)
            return None

        finally:
            cursor.close()
            conn.close()

        return user_name, date_created

    def update_existing_user_by_id(self):
        """ SQL Query for updating username by user id from users table """

        user_id = self.user_id
        new_user_name = self.new_user_name
        date_created = self.date_created

        try:
            if isinstance(user_id, int):
                user_id = str(user_id)
        except ValueError as valErr:
            return "Error"

        if not user_id.isalnum():
            return "Error"

        obj_get_existing_user = DBConnector(user_id, None, None, None)
        old_user_name_result = obj_get_existing_user.get_existing_user_by_id()

        if old_user_name_result is not None:
            old_user_name = old_user_name_result[0]
        else:
            return None

        if new_user_name == old_user_name:
            return False

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika UPDATE
        users = Table(get_app_settings_obj.get_users_db_table_name())
        update_user_query = Query.update(get_app_settings_obj.get_db_schema_pypika_format().users)\
            .set(users.user_name, new_user_name)\
            .set(users.creation_date, date_created)\
            .where(users.user_id == user_id)

        update_user_query = update_user_query.get_sql()  # get Query as SQL
        update_user_query = update_user_query.replace('"', '')  # Removing apostrophes from relevant strings

        cursor.execute(update_user_query)

        affected_rows = cursor.rowcount
        if affected_rows == 0:
            print(affected_rows)
            return "Error"

        else:
            print("user id:", user_id,
                  "user name change to:", new_user_name,
                  "affected rows:", affected_rows)

        conn.commit()
        cursor.close()
        conn.close()
        return True

    def delete_existing_user_by_id(self):
        """ SQL Query for deleting user by user id from users table """

        user_id = self.user_id

        if not user_id.isalnum():
            return "Error"

        try:
            if isinstance(user_id, str):
                user_id = int(user_id)
        except ValueError as valErr:
            user_id = str(user_id)
            return "Error"

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika DELETE
        users = Table(get_app_settings_obj.get_users_db_table_name())
        delete_user_query = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).delete().where(
            users.user_id == user_id
        )

        delete_user_query = delete_user_query.get_sql()
        delete_user_query = delete_user_query.replace('"', '')  # Removing apostrophes from relevant strings

        cursor.execute(delete_user_query)

        affected_rows = cursor.rowcount

        if affected_rows == 0:
            # print(affected_rows)
            return False

        else:
            print("user id:", user_id, "was deleted successfully, affected rows:", affected_rows)

        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_users_table_as_json():
        """ Printing users table as JSON from db """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika SELECT
        select_all_users_query = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select('*')
        select_all_users_query = select_all_users_query.get_sql()
        select_all_users_query = select_all_users_query.replace('"', '')

        try:
            cursor.execute(select_all_users_query)
            conn.commit()

            if cursor.rowcount >= 1:
                result = cursor.fetchall()

                users_table_list = []

                for row in result:
                    users_table_list.append(
                        {"id": row[0],
                         "user_name": row[1],
                         "date_created": str(row[2])
                         }
                    )

                # convert list to JSON
                table_to_json = json.dumps(users_table_list)

                return table_to_json

            else:
                return False

        except pymysql.err.IntegrityError as sqlError:
            print("Error:", sqlError)

        finally:
            # Close connection and cursor
            cursor.close()
            conn.close()

    @staticmethod
    def get_config_table_as_json():
        """ Printing users table as JSON from db """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika SELECT
        select_all_from_config = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().config).select('*')
        select_all_from_config = select_all_from_config.get_sql()
        select_all_from_config = select_all_from_config.replace('"', '')

        try:
            cursor.execute(select_all_from_config)
            conn.commit()

            if cursor.rowcount >= 1:
                result = cursor.fetchall()

                config_table_list = []

                for row in result:
                    config_table_list.append(
                        {
                            "id": row[0],
                            "protocol": row[1],
                            "flaskHostAddress": row[2],
                            "serverTestingHostAddress": row[3],
                            "restAppPort": row[4],
                            "webAppPort": row[5],
                            "usersEndpoint": row[6],
                            "getUsersDataEndpoint": row[7],
                            "createUsersEndpoint": row[8],
                            "getAllUsersEndpoint": row[9],
                            "stopRestServerEndpoint": row[10],
                            "stopWebServerEndpoint": row[11],
                            "testingBrowser": row[12],
                            "testingUserName": row[13]
                        }
                    )

                # convert list to JSON
                table_to_json = json.dumps(config_table_list)

                return table_to_json

            else:
                return False

        except pymysql.err.IntegrityError as sqlError:
            print("Error:", sqlError)

        finally:
            # Close connection and cursor
            cursor.close()
            conn.close()

    def create_user_based_on_available_id(self):
        """ SQL Query for creates new user by username - user id will be auto generated based on next available id """

        user_name = self.user_name
        date_created = self.date_created

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        obj_get_next_user_id = DBConnector
        user_id = obj_get_next_user_id.get_next_available_user_id_from_db()

        # PyPika INSERT
        insert_based_on_available_id_query = Query.into(get_app_settings_obj.get_db_schema_pypika_format().users).insert(
            user_id,
            user_name,
            date_created
        )

        insert_based_on_available_id_query = insert_based_on_available_id_query.get_sql()  # get Query as SQL
        insert_based_on_available_id_query = insert_based_on_available_id_query.replace('"', '')  # Removing apostrophes from relevant strings

        try:
            cursor.execute(insert_based_on_available_id_query)
            conn.commit()
            # print(cursor.rowcount, "record inserted.")

        except pymysql.err.IntegrityError as sqlError:
            # Catch Exception if user exist or not
            print("Error:", sqlError)
            return False

        finally:
            # Close connection and cursor
            cursor.close()
            conn.close()

        return True

    @staticmethod
    def get_next_available_user_id_from_db():
        """ SQL Query that gets all next available id based on all id's in DB """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika SELECT
        users = Table(get_app_settings_obj.get_users_db_table_name())
        get_all_users_ids = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select(
            users.user_id
        )

        get_all_users_ids = get_all_users_ids.get_sql()
        get_all_users_ids = get_all_users_ids.replace('"', '')  # Removing apostrophes from relevant strings

        cursor.execute(get_all_users_ids)
        conn.commit()

        get_db_current_users_id = []

        # get all users id's from db into list
        for row in cursor:
            get_db_current_users_id.append(row)

        # clear list of user id's formatting
        get_db_current_users_id = list(itertools.chain(*get_db_current_users_id))
        # print("current list from db", get_db_current_users_id)

        try:
            # if db is empty set default user_id value to 1
            if not get_db_current_users_id:
                next_available_user_id = 1

            else:
                # find missing ids in 'get_db_current_users_id' based on db query result
                missing_id_nums_in_list = sorted(
                    set(range(1, get_db_current_users_id[-1])) - set(get_db_current_users_id))
                # print("missing numbers:", missing_id_nums_in_list)

                # if there is no missing numbers in 'missing_id_nums_in_list',
                # we'll add +1 to the largest number in 'get_db_current_users_id' (from db)
                if not missing_id_nums_in_list:
                    # print("no missing id's in list missing_id_nums_in_list:", missing_id_nums_in_list)
                    next_available_user_id = max(get_db_current_users_id) + 1
                    # print("new user id defined:", next_available_user_id)

                else:  # if there is missing numbers in list we'll use the lowest number from 'missing_id_nums_in_list'
                    next_available_user_id = min(missing_id_nums_in_list)
                    # print("### new user id:", next_available_user_id)

        except ValueError as val:
            print(val)
        except UnboundLocalError as localErr:
            print(localErr)
        finally:
            cursor.close()
            conn.close()

        return next_available_user_id

    @staticmethod
    def get_random_exist_user_id():
        """ SQL Query that return random id based on all id's in DB """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika SELECT
        users = Table(get_app_settings_obj.get_users_db_table_name())
        get_all_users_ids = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select(
            users.user_id
        )

        get_all_users_ids = get_all_users_ids.get_sql()
        get_all_users_ids = get_all_users_ids.replace('"', '')  # Removing apostrophes from relevant strings

        cursor.execute(get_all_users_ids)
        conn.commit()

        get_db_users_id = []

        # get all users id's from db into list
        for row in cursor:
            get_db_users_id.append(row)

        # clear list of user id's formatting
        get_db_users_id = list(itertools.chain(*get_db_users_id))
        # print("current list from db", get_db_current_users_id)

        try:
            random_exist_user_id = random.choice(get_db_users_id)
            # print("random id:", random_exist_user_id)

        except ValueError as val:
            print(val)
        except UnboundLocalError as localErr:
            print(localErr)
        finally:
            cursor.close()
            conn.close()

        return random_exist_user_id
