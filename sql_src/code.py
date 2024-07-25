
import mysql.connector
import pandas as pd

def connect_sql_server(host_name: str, user_name: str, password: str):
    try: 
        con = mysql.connector.connect(
        host=host_name,
        user=user_name,
        password=password,
        database = 'red_bus_scrape'
        )
        cursor = con.cursor()
        return cursor,con
    except Exception as e:
        raise e


def create_database(database_name: str, cursor, use_database = True):
    try:
        query = f"create database if not exists {database_name}"
        cursor.execute(query)
        if use_database: 
            cursor.execute(f'use {database_name}')
    except Exception as e:
        raise e


def create_table(cursor,table_name:str,attributes:str):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} ({attributes})''' )


def insert_values(cursor, table_name:str, attributes:tuple,values:list):
    cursor.executemany(f'''INSERT INTO {table_name} {str(attributes)} VALUES {str(('%s')*len(attributes))}''', values)



def add_route(cursor, values:list = None):
    create_database(database_name='red_bus_scrape',cursor=cursor)
    create_table(cursor=cursor,table_name='route', attributes='id INT PRIMARY_KEY, route VARCHAR(255), route_link VARCHAR(255)')
    if values:
        insert_values(cursor,table_name='route',attributes=('id', 'route', 'route_link'),values=values)


def add_bus_info(cursor, values:list = None):
    create_database(database_name='bus_info',cursor=cursor)
    create_table(cursor=cursor,table_name='bus_info',attributes='''id INT PRIMARY KEY,
                                                                    route_id INT,
                                                                    bus_name VARCHAR(255) NOT NULL,
                                                                    bus_type VARCHAR(255) NOT NULL,
                                                                    duration VARCHAR(50),
                                                                    departure_time VARCHAR(25),
                                                                    reaching_time VARCHAR(25),
                                                                    price DECIMAL(10, 2) NOT NULL,
                                                                    available_seats INT,
                                                                    rating DECIMAL(3, 1),
                                                                    FOREIGN KEY (route_id) REFERENCES route(id)''')
    
    if values:
        insert_values(cursor,'bus_info',attributes=('id', 'route_id', 'bus_name', 'bus_type', 'duration', 
                                                    'departure_time', 'reaching_time', 'price', 'available_seats', 'rating'),
                                                    
                                        values=values)



def fetch_data():
    _,conn = connect_sql_server('localhost','root','password')
    query = """
    SELECT 
        bus_info.id AS bus_id, 
        route.route, 
        route.route_link, 
        bus_info.bus_name, 
        bus_info.bus_type, 
        bus_info.duration, 
        bus_info.departure_time, 
        bus_info.reaching_time, 
        bus_info.price, 
        bus_info.available_seats, 
        bus_info.rating 
    FROM 
        bus_info 
    JOIN 
        route ON bus_info.route_id = route.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df









