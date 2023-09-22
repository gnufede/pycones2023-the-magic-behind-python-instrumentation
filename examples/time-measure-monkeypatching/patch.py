#!/usr/bin/env python3

import time
import sqlite


# Monkeypatch the inner_query function to add timing measurement
def inner_query_patched():
    start_time = time.time()
    result = sqlite._original_inner_query()  # Call the original function
    end_time = time.time()
    print(f"Function inner_query took {end_time - start_time} seconds to execute")
    return result


# Replace the original inner_query with the patched version
setattr(sqlite, "_original_inner_query", sqlite.inner_query)
setattr(sqlite, "inner_query", inner_query_patched)

# Call the inner_query function to execute the SQL query
query_results = sqlite.inner_query()

# Process and print the results outside the function
if query_results:
    for row in query_results:
        print(row)
