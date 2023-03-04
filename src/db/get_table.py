import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import html
from src.App.AppSettings import ApplicationSettings
from pypika import Query
from prettytable import PrettyTable
import os.path
import platform


class GetTablesFromDB:

    def __init__(self,
                 print_users_table_to_txt_file,
                 print_users_table_to_terminal,
                 print_users_table_to_html_file,
                 print_config_table_to_txt_file,
                 print_config_table_to_terminal,
                 print_config_table_to_html_file):

        self.print_users_table_to_txt_file = print_users_table_to_txt_file
        self.print_users_table_to_terminal = print_users_table_to_terminal
        self.print_users_table_to_html_file = print_users_table_to_html_file
        self.print_config_table_to_txt_file = print_config_table_to_txt_file
        self.print_config_table_to_terminal = print_config_table_to_terminal
        self.print_config_table_to_html_file = print_config_table_to_html_file

    @staticmethod
    def get_app_path():
        """  define root source path """
        return package_path

    def get_users_table(self):
        """ Printing users table from db """
        print_users_table_to_txt_file = self.print_users_table_to_txt_file
        print_users_table_to_terminal = self.print_users_table_to_terminal
        print_users_table_to_html_file = self.print_users_table_to_html_file

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()
        conn.commit()

        # PyPika SELECT
        get_db_users_table = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select('*')
        get_db_users_table = get_db_users_table.get_sql()
        get_db_users_table = get_db_users_table.replace('"', '')

        cursor.execute(get_db_users_table)

        result = cursor.fetchall()
        table = PrettyTable([
            'user id',
            'user name',
            'creation date'
        ])

        table.hrules = 1
        table.vrules = 1

        for r in result:
            t = (r[0], r[1], str(r[2]))
            table.add_row(t)

        if print_users_table_to_terminal:
            print(table, "\n")

        cursor.close()
        conn.close()

        # print table to txt file
        if print_users_table_to_txt_file:
            try:
                if platform.system() == 'Windows':
                    win_users_txt_file_name = "\\users_table.txt"
                    win_users_txt_file_folder = package_path + "\\src\\txt_files"
                    if not os.path.exists(win_users_txt_file_folder):
                        os.makedirs(win_users_txt_file_folder)

                    file = open(win_users_txt_file_folder + win_users_txt_file_name, "w+")
                    file.write(str(table))
                    print("table output was saved to:", win_users_txt_file_folder + win_users_txt_file_name)

                elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                    unix_users_txt_file_name = "/users_table.txt"
                    unix_users_txt_file_folder = package_path + "/src/txt_files"
                    if not os.path.exists(unix_users_txt_file_folder):
                        os.makedirs(unix_users_txt_file_folder)

                    file = open(unix_users_txt_file_folder + unix_users_txt_file_name, "w+")
                    file.write(str(table))
                    print("table output was saved to:", unix_users_txt_file_folder + unix_users_txt_file_name)

            except IOError as err:
                print("Error:", err)

            finally:
                file.close()

        # print users table to HTML file
        if print_users_table_to_html_file:
            try:
                if platform.system() == 'Windows':
                    win_users_html_file_name = "\\users_table.html"
                    win_users_html_folder = package_path + "\\src\\html_files"
                    if not os.path.exists(win_users_html_folder):
                        os.makedirs(win_users_html_folder)

                    html_to_save = table.get_html_string(attributes={"class": "table"}, format=True)
                    html_to_save = html.unescape(html_to_save)

                    html_file = open(win_users_html_folder + win_users_html_file_name, "w+")
                    html_file.write(html_to_save)
                    # print(html_to_save)

                elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                    unix_users_html_file_name = "/users_table.html"
                    unix_users_html_folder = package_path + "/src/html_files"
                    if not os.path.exists(unix_users_html_folder):
                        os.makedirs(unix_users_html_folder)

                    html_to_save = table.get_html_string(attributes={"class": "table"}, format=True)
                    html_to_save = html.unescape(html_to_save)

                    html_file = open(unix_users_html_folder + unix_users_html_file_name, "w+")
                    html_file.write(html_to_save)
                    # print(html_to_save)

            except IOError as err:
                print(err)

            finally:
                html_file.close()

    def get_config_table(self):
        """ Printing config table from db """
        print_config_table_to_txt_file = self.print_config_table_to_txt_file
        print_config_table_to_terminal = self.print_config_table_to_terminal
        print_config_table_to_html_file = self.print_config_table_to_html_file

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # Establishing connection to db
        cursor, conn = get_app_settings_obj.connect_to_database()
        conn.commit()

        # PyPika SELECT
        get_db_config_table = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().config).select('*')
        get_db_config_table = get_db_config_table.get_sql()
        get_db_config_table = get_db_config_table.replace('"', '')

        cursor.execute(get_db_config_table)

        result = cursor.fetchall()
        table = PrettyTable([
            'id',
            'protocol',
            'flask host address',
            'server testing host address',
            'rest app port',
            'web app port',
            'users endpoint',
            'get users data endpoint',
            'auto create users endpoint',
            'get all users endpoint',
            'stop rest server endpoint',
            'stop web server endpoint',
            'testing browser',
            'testing username'
        ])

        table.hrules = 1
        table.vrules = 1

        for row in result:
            table.add_row(row)

        if print_config_table_to_terminal:
            print(table, "\n")

        cursor.close()
        conn.close()

        # print table to txt file
        if print_config_table_to_txt_file:
            try:
                if platform.system() == 'Windows':
                    win_config_txt_file_name = "\\config_table.txt"
                    win_config_txt_file_folder = package_path + "\\src\\txt_files"
                    if not os.path.exists(win_config_txt_file_folder):
                        os.makedirs(win_config_txt_file_folder)

                    file = open(win_config_txt_file_folder + win_config_txt_file_name, "w+")
                    file.write(str(table))
                    print("table output was saved to:", win_config_txt_file_folder + win_config_txt_file_name)

                elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                    unix_config_txt_file_name = "/config_table.txt"
                    unix_config_txt_file_folder = package_path + "/src/txt_files"
                    if not os.path.exists(unix_config_txt_file_folder):
                        os.makedirs(unix_config_txt_file_folder)

                    file = open(unix_config_txt_file_folder + unix_config_txt_file_name, "w+")
                    file.write(str(table))
                    print("table output was saved to:", unix_config_txt_file_folder + unix_config_txt_file_name)

            except IOError as err:
                print(err)

            finally:
                file.close()

        # print config table to HTML file
        if print_config_table_to_html_file:
            try:
                if platform.system() == 'Windows':
                    win_config_html_file_name = "\\config_table.html"
                    win_config_html_folder = package_path + "\\src\\html_files"

                    if not os.path.exists(win_config_html_folder):
                        os.makedirs(win_config_html_folder)

                    html_to_save = table.get_html_string(attributes={"class": "table"}, format=True)
                    html_to_save = html.unescape(html_to_save)

                    html_file = open(win_config_html_folder + win_config_html_file_name, "w+")
                    html_file.write(html_to_save)
                    # print(html_to_save)

                elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                    unix_config_html_file_name = "/config_table.html"
                    unix_config_html_folder = package_path + "/src/html_files"

                    if not os.path.exists(unix_config_html_folder):
                        os.makedirs(unix_config_html_folder)

                    html_to_save = table.get_html_string(attributes={"class": "table"}, format=True)
                    html_to_save = html.unescape(html_to_save)

                    html_file = open(unix_config_html_folder + unix_config_html_file_name, "w+")
                    html_file.write(html_to_save)
                    # print(html_to_save)

            except IOError as err:
                print(err)

            finally:
                html_file.close()
