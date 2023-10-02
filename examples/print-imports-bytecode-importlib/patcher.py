#!/usr/bin/env python3

from bytecode import Bytecode, Instr
from importlib._bootstrap_external import SourceLoader
from importlib._bootstrap_external import SourcelessFileLoader


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


for i in SourceLoader, SourcelessFileLoader:
    setattr(i, "_orig_get_code", i.get_code)
    setattr(i, "get_code", new_get_code)
