from db.connection import Database

def test_connection():
    conn = Database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1;")
    result = cursor.fetchone()

    print("DB Test Result:", result)

    cursor.close()
    Database.release_connection(conn)

if __name__ == "__main__":
    test_connection()