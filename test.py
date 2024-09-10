import sqlite_functions as sql
import dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    config = dotenv.dotenv_values()
    sql.add_to_the_database(config["PATH_TO_DB"],"visited" , cookie = 1)
    visited = sql.get_from_database(config["PATH_TO_DB"],"visited",id = 7)

