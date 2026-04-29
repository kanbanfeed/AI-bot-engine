import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _connection_pool = None

    @staticmethod
    def initialize():
        try:
            Database._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            print("Database connection pool created")
        except Exception as e:
            print("Error creating connection pool:", str(e))
            raise e

    @staticmethod
    def get_connection():
        if Database._connection_pool is None:
            Database.initialize()
        return Database._connection_pool.getconn()

    @staticmethod
    def release_connection(conn):
        if Database._connection_pool:
            Database._connection_pool.putconn(conn)

    @staticmethod
    def close_all():
        if Database._connection_pool:
            Database._connection_pool.closeall()
            print(" Database connections closed")