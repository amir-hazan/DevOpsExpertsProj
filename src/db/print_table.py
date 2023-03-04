import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

from src.db.get_table import GetTablesFromDB


class PrintDBTables:
    @staticmethod
    def print_table_from_db():
        """ Printing table from DB Based on user selection """
        while True:
            try:
                user_input = int(input(
                    "### CHOOSE WHICH TABLE YOU WANT TO PRINT AND SAVE:\n"
                    "1. USERS TABLE\n"
                    "2. CONFIG TABLE\n"
                    "3. BOTH TABLES\n"
                    "### TYPE YOUR ANSWER: "
                ))

            except ValueError as valErr:
                # print("Error:", valErr, "\n\n")
                print("ANSWER MUST BE NUMBER, TRY AGAIN\n")
                continue

            if user_input not in range(1, 4):
                print("WRONG ANSWER, MUST BE BETWEEN 1 AND 3, TRY AGAIN!\n")

            else:
                obj_print_users_tbl = GetTablesFromDB(True, True, False, False, False, False)
                obj_print_config_tbl = GetTablesFromDB(False, False, False, True, True, False)

                if user_input == 1:
                    obj_print_users_tbl.get_users_table()
                elif user_input == 2:
                    obj_print_config_tbl.get_config_table()
                elif user_input == 3:
                    obj_print_users_tbl.get_users_table()
                    obj_print_config_tbl.get_config_table()
                return


PrintDBTables.print_table_from_db()
