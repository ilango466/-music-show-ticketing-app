import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from traceback import print_exc


load_dotenv()
database_uri = os.getenv('DATABASE_URI')
# database_uri = 'postgres://ilango:asdf!446@192.168.17.192:5432/music_show_ticketing'


print(database_uri)
db_pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn = database_uri)


@contextmanager
def get_connection():
    connection = db_pool.getconn()
    try: 
        yield connection
    except Exception as error:
        print("Error in getting connection from pool : ",error)
        print_exc(error)
    finally:
        db_pool.putconn(connection)


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor