#!/usr/bin/env python3
import ast
import astor
import inspect


from sqlite import inner_query


class TimingVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        # Identify the method you want to modify
        if node.name == "inner_query":
            # Add timing measurement code before and after the original code
            import_time_code = ast.parse("import time")
            start_time_code = ast.parse("start_time = time.time()")
            end_time_code = ast.parse("end_time = time.time()")
            print_time_code = ast.parse(
                "print(f'Method inner_query took {end_time - start_time} seconds to execute')"
            )
            node.body.insert(0, start_time_code.body[0])
            node.body.insert(0, import_time_code.body[0])
            node.body.append(end_time_code.body[0])
            node.body.append(print_time_code.body[0])
        self.generic_visit(node)


if __name__ == "__main__":
    # Apply AST patching to modify the inner_query method
    tree = ast.parse(inspect.getsource(inner_query))
    TimingVisitor().visit(tree)
    modified_code = astor.to_source(tree)

    compiled_code = compile(modified_code, "<string>", "exec")
    exec(compiled_code, globals())

    # Call the inner_query method to execute the SQL query
    query_results = inner_query()
