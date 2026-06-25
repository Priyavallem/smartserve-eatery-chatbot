import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "smartserve_eatery"),
}


@contextmanager
def get_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()


def insert_order_item(food_item, quantity, order_id):
    """Insert one item in an order using the database stored procedure."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.callproc("insert_order_item", (food_item, quantity, order_id))
            connection.commit()
            cursor.close()
            return True

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def insert_order_tracking(order_id, status):
    with get_connection() as connection:
        cursor = connection.cursor()
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))
        connection.commit()
        cursor.close()


def get_total_order_price(order_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT get_total_order_price(%s)", (order_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result


def get_next_order_id():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(order_id), 0) + 1 FROM orders")
        result = cursor.fetchone()[0]
        cursor.close()
        return result


def get_order_status(order_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT status FROM order_tracking WHERE order_id = %s",
            (order_id,),
        )
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None


if __name__ == "__main__":
    print(get_next_order_id())
