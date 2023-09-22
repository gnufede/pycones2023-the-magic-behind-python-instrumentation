#!/usr/bin/env python3
import sqlite3
from interface import timing_decorator

# Define the path to your SQLite database file
db_file = ":memory:"


@timing_decorator
def inner_query():
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Write your SQL query
        sql_query = """
        SELECT type, name, sql
        FROM sqlite_master
        WHERE 1;
        """

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch the results (if the query returns data)
        results = cursor.fetchall()

        # Process and return the results
        return results

    except sqlite3.Error as e:
        print("Error connecting to SQLite:", e)
        return None

    finally:
        # Close the cursor and the database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
