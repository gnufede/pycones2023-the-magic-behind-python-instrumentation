#!/usr/bin/env python3

from bytecode import Bytecode, Instr
from importlib._bootstrap_external import _LoaderBasics


def print_stmt_bytecode(fullname):
    return [
        Instr("LOAD_NAME", arg="print"),
        Instr("LOAD_CONST", arg=fullname),
        Instr("CALL_FUNCTION", arg=1),
    ]


def new_get_code(self, fullname):
    orig_code = self._orig_get_code(fullname)
    new_bytecode = Bytecode.from_code(orig_code)
    new_bytecode[:0] = print_stmt_bytecode(fullname)
    return new_bytecode.to_code()


# setattr(SourceLoader, "_orig_get_code", SourceLoader.get_code)
# setattr(SourceLoader, "get_code", new_get_code)

setattr(_LoaderBasics, "_orig_get_code", SourceLoader.get_code)
setattr(_LoaderBasics, "get_code", new_get_code)
