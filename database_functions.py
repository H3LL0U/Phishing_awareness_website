import mysql.connector
from mysql.connector import Error, MySQLConnection
import sqlite3
def connect_to_database(host,user,password,database,port):
    
        
    connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            
        )

    return connection





def send_query(connection:MySQLConnection,query:str):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
def get_all_tables_sqlite(path_to_db="leerling_emails_db\leerling_emails.db"):
    connection = sqlite3.connect(path_to_db)
    cur = connection.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()
def transfer_old_to_new(connection:MySQLConnection,path_to_db="leerling_emails_db\leerling_emails.db"):
    previous_tables = get_all_tables_sqlite(path_to_db=path_to_db)
    for colums in previous_tables:
        id_,email,subscribed = colums
        query = f'''
        INSERT INTO users ( email, subscribed)
        VALUES ("{email}", {int(subscribed)});
        '''
        send_query(connection=connection,query=query)
def add_new_user(connection:MySQLConnection,email,subscribed = True):
    query = f'''
        INSERT IGNORE INTO users ( email, subscribed)
        VALUES ("{email}", {int(subscribed)})
        
        '''
    
    send_query(connection=connection,query=query)


def create_table(connection:MySQLConnection):
    query=\
'''
CREATE TABLE IF NOT EXISTS visited (
    ID INT NOT NULL AUTO_INCREMENT,
    cookie VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (ID)
);
'''


    send_query(connection=connection,query=query)

def get_max_id(connection:MySQLConnection,table_name):
    '''
    returns the biggest ID in a table
    '''
    try:
        conn = connection
        cur = conn.cursor()

        
        query = f"SELECT MAX(ID) FROM {table_name};"
        cur.execute(query)

        
        max_id = cur.fetchone()[0]

        
        return max_id if max_id is not None else 0

    except Exception as error:
        print(f"Error fetching max id: {error}")
        return 0

def get_from_database(connection:MySQLConnection, table_name, **conditions):
    try:
        conn = connection
        cur = conn.cursor()

        
        if conditions:
            where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
            select_query = f"SELECT * FROM {table_name} WHERE {where_clause};"
            cur.execute(select_query, list(conditions.values()))
        else:
            
            select_query = f"SELECT * FROM {table_name};"
            cur.execute(select_query)

        
        rows = cur.fetchall()

        
        return rows
    
    except Exception as error:
        print(f"Error fetching data: {error}")
        return None

def add_to_the_database(connection:MySQLConnection,table_name, **table_values):
    try:
        conn = connection
        cur = conn.cursor()

    

        
        insert_query = f"INSERT INTO {table_name} ({', '.join(table_values.keys())}) VALUES ({', '.join([r'%s' for _ in table_values.values()])});"
        cur.execute(insert_query, list(table_values.values()))

        conn.commit()
        #print("Done!")
    except Exception as error:
        print(error)