import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host=tokened.bddip,
                                         port=tokened.bddport,
                                         user=tokened.bdduser,
                                         password=tokened.bddpassword,
                                         database='sd701')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    print("MySQL connection is closed")