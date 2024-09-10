import sqlite3


def add_to_the_database(path_to_db,table_name, **table_values):
    try:
        conn = sqlite3.connect(path_to_db)
        cur = conn.cursor()

       
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, "
        create_table_query += ", ".join([f"{key} TEXT" for key in table_values.keys()])
        create_table_query += ");"
        cur.execute(create_table_query)

        
        insert_query = f"INSERT INTO {table_name} ({', '.join(table_values.keys())}) VALUES ({', '.join(['?' for _ in table_values.values()])});"
        cur.execute(insert_query, list(table_values.values()))

        conn.commit()
        #print("Done!")
    except sqlite3.Error as error:
        print(error)

    finally:
        conn.close()
def get_from_database(path_to_db, table_name, **conditions):
    try:
        conn = sqlite3.connect(path_to_db)
        cur = conn.cursor()

        
        if conditions:
            where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
            select_query = f"SELECT * FROM {table_name} WHERE {where_clause};"
            cur.execute(select_query, list(conditions.values()))
        else:
            
            select_query = f"SELECT * FROM {table_name};"
            cur.execute(select_query)

        
        rows = cur.fetchall()

        # Return the fetched rows
        return rows
    
    except sqlite3.Error as error:
        print(f"Error fetching data: {error}")
        return None

    finally:
        conn.close()

def get_max_id(path_to_db, table_name):
    try:
        conn = sqlite3.connect(path_to_db)
        cur = conn.cursor()

        
        query = f"SELECT MAX(id) FROM {table_name};"
        cur.execute(query)

        
        max_id = cur.fetchone()[0]

        
        return max_id if max_id is not None else 0

    except sqlite3.Error as error:
        print(f"Error fetching max id: {error}")
        return 0

    finally:
        conn.close()

