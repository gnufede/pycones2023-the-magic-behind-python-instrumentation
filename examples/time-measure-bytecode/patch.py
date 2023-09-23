#!/usr/bin/env python3

from bytecode import Bytecode, Instr

top_bytecode = [
    Instr("LOAD_CONST", 0),
    Instr("LOAD_CONST", arg=None),
    Instr("IMPORT_NAME", arg="time"),
    Instr("STORE_FAST", arg="time"),
    Instr("LOAD_FAST", arg="time"),
    Instr("LOAD_METHOD", arg="time"),
    Instr("CALL_METHOD", arg=0),
    Instr("STORE_FAST", arg="start_time"),
    Instr("LOAD_CONST", arg=0),
    Instr("LOAD_CONST", arg=None),
]


bottom_bytecode = [
    Instr("LOAD_FAST", arg="time"),
    Instr("LOAD_METHOD", arg="time"),
    Instr("CALL_METHOD", arg=0),
    Instr("STORE_FAST", arg="end_time"),
    Instr("LOAD_GLOBAL", arg="print"),
    Instr("LOAD_CONST", arg="Function took "),
    Instr("LOAD_FAST", arg="end_time"),
    Instr("LOAD_FAST", arg="start_time"),
    Instr("BINARY_SUBTRACT"),
    Instr("FORMAT_VALUE", arg=0),
    Instr("LOAD_CONST", arg=" seconds to execute"),
    Instr("BUILD_STRING", arg=3),
    Instr("CALL_FUNCTION", arg=1),
    Instr("POP_TOP"),
    Instr("LOAD_CONST", arg=None),
    Instr("RETURN_VALUE"),
]

# Function to add timing measurement to a function's bytecode
def add_timing_measurement(func):
    # Get the bytecode of the function
    code = func.__code__
    bytecode = Bytecode.from_code(code)

    bytecode[:2] = top_bytecode
    bytecode[-2:] = bottom_bytecode

    func.__code__ = bytecode.to_code()

    return func


from sqlite import inner_query

# Apply bytecode patching to modify the inner_query function
inner_query = add_timing_measurement(inner_query)

# Call the inner_query function to execute the SQL query
query_results = inner_query()

# Process and print the results outside the function
if query_results:
    for row in query_results:
        print(row)
