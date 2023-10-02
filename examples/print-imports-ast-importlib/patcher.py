#!/usr/bin/env python3

import ast
from importlib._bootstrap import _call_with_frames_removed

from importlib.machinery import SourceFileLoader


def insert_print_stmt(tree, module_name):
    # Create an import statement node
    # import_node = ast.Import(names=[ast.alias(name=module_name, asname=None)])
    import_node = ast.Expr(
        lineno=1,
        col_offset=0,
        end_lineno=1,
        end_col_offset=20,
        value=ast.Call(
            lineno=1,
            col_offset=0,
            end_lineno=1,
            end_col_offset=20,
            func=ast.Name(
                lineno=1,
                col_offset=0,
                end_lineno=1,
                end_col_offset=5,
                id="print",
                ctx=ast.Load(),
            ),
            args=[
                ast.Constant(
                    lineno=1,
                    col_offset=6,
                    end_lineno=1,
                    end_col_offset=19,
                    value=module_name,
                    kind=None,
                )
            ],
            keywords=[],
        ),
    )
    # Insert the import statement at the beginning of the module's AST
    tree.body.insert(-1, import_node)


def patch_ast(module, module_name):
    # Open and parse the source code of the module
    with open(module.__file__, "r") as source_file:
        source_code = source_file.read()
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    # Insert your AST manipulation logic here
    insert_print_stmt(tree, module_name)
    # Compile the modified AST back to source code
    return compile(tree, filename=module.__file__, mode="exec")


def exec_module(self, module):
    # Patch the AST here
    code = patch_ast(module, self.name)
    # Execute the modified source code within the module's namespace
    _call_with_frames_removed(exec, code, module.__dict__)


setattr(SourceFileLoader, "exec_module", exec_module)
