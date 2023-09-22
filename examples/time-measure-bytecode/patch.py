#!/usr/bin/env python3

import dis
import types
from bytecode import Bytecode


def calc_lnotab(insns, firstlineno=0):
    """Calculate the line number table for the bytecode"""
    # Details of the format of co_lnotab are explained in Objects/lnotab_notes.txt, so I won't bother repeating all of that
    new_lnotab = []
    prev_offset, prev_lineno = 0, firstlineno
    for insn in insns:
        if insn.starts_line:
            offset, lineno = insn.offset - prev_offset, insn.starts_line - prev_lineno
            prev_offset, prev_lineno = insn.offset, insn.starts_line
            assert (offset > 0 or prev_offset == 0) and lineno > 0
            while offset > 255:
                new_lnotab.extend((255, 0))
                offset -= 255
            while lineno > 255:
                new_lnotab.extend((offset, 255))
                offset = 0
                lineno -= 255
            new_lnotab.extend((offset, lineno))
    return bytes(new_lnotab)


# Function to add timing measurement to a function's bytecode
def add_timing_measurement(func):
    # Get the bytecode of the function
    code = func.__code__
    bytecode = Bytecode.from_code(code)

    extra_bytecode_before = ConcreteBytecode(
        [
            ConcreteInstr("LOAD_CONST", 0),
            ConcreteInstr("LOAD_CONST", 1),
            ConcreteInstr("IMPORT_NAME", "time"),
            ConcreteInstr("STORE_NAME", "time"),
            ConcreteInstr("LOAD_CONST", 1),
            ConcreteInstr("POP_TOP"),
            ConcreteInstr("LOAD_CONST", None),
            ConcreteInstr("RETURN_VALUE"),
        ]
    )

    code = bytecode.to_code()
    exec(code)

    # Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval=0, argrepr='0', offset=0, starts_line=1, is_jump_target=False)
    # Instruction(opname='LOAD_CONST', opcode=100, arg=1, argval=None, argrepr='None', offset=2, starts_line=None, is_jump_target=False)
    # Instruction(opname='IMPORT_NAME', opcode=108, arg=0, argval='time', argrepr='time', offset=4, starts_line=None, is_jump_target=False)
    # Instruction(opname='STORE_NAME', opcode=90, arg=0, argval='time', argrepr='time', offset=6, starts_line=None, is_jump_target=False)
    # Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='time', argrepr='time', offset=8, starts_line=None, is_jump_target=False)
    # Instruction(opname='LOAD_METHOD', opcode=160, arg=0, argval='time', argrepr='time', offset=10, starts_line=None, is_jump_target=False)
    # Instruction(opname='CALL_METHOD', opcode=161, arg=0, argval=0, argrepr='', offset=12, starts_line=None, is_jump_target=False)
    # Instruction(opname='STORE_NAME', opcode=90, arg=1, argval='start_time', argrepr='start_time', offset=14, starts_line=None, is_jump_target=False)
    # Instruction(opname='LOAD_CONST', opcode=100, arg=1, argval=None, argrepr='None', offset=16, starts_line=None, is_jump_target=False)
    # Instruction(opname='RETURN_VALUE', opcode=83, arg=None, argval=None, argrepr='', offset=18, starts_line=None, is_jump_target=False)

    # Disassemble the bytecode
    instructions = dis.get_instructions(code)

    # Create a list to hold modified instructions
    modified_instructions = []

    # Add timing measurement instructions before and after the original code
    modified_instructions.extend(dis.get_instructions("import time"))
    modified_instructions.extend(dis.get_instructions("start_time = time.time()"))
    modified_instructions.extend(instructions)
    modified_instructions.extend(dis.get_instructions("end_time = time.time()"))
    modified_instructions.extend(
        dis.get_instructions(
            "print(f'Function {func.__name__} took {end_time - start_time} seconds to execute')"
        )
    )

    # Create a new code object with the modified instructions
    modified_code = types.CodeType(
        code.co_argcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_stacksize,
        code.co_flags,
        bytes(0),
        # calc_lnotab(modified_instructions),
        bytes(0),
        # code.co_consts,
        code.co_names,
        code.co_varnames,
        (code.co_filename,),
        code.co_name,
        str(code.co_firstlineno),
        code.co_lnotab,
        code.co_freevars,
        code.co_cellvars,
    )

    # Create a new function with the modified code object
    modified_func = types.FunctionType(
        modified_code,
        func.__globals__,
        func.__name__,
        func.__defaults__,
        func.__closure__,
    )

    return modified_func


from sqlite import inner_query

# Apply bytecode patching to modify the inner_query function
inner_query = add_timing_measurement(inner_query)

# Call the inner_query function to execute the SQL query
query_results = inner_query()

# Process and print the results outside the function
if query_results:
    for row in query_results:
        print(row)
