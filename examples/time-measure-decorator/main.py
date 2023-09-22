#!/usr/bin/env python3

import sqlite

if __name__ == "__main__":
    # obj = sqlite.MeasuredSQLite()
    # obj.query_wrapper()

    # Call the inner_query function to execute the SQL query
    query_results = sqlite.inner_query()

    # Process and print the results outside the function
    if query_results:
        for row in query_results:
            print(row)
