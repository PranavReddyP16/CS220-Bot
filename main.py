import badexception, longfunctions, repeatedcodesegment, unusedimport

#find_bad_exception_handling
with open('test_bad_exception_handling.py') as f:
    code = f.read()

bad_handlers = badexception.find_bad_exception_handling(code)
for lineno in bad_handlers:
    print(f"Bad exception: Bad exception handling found on line {lineno}")

#find_long_functions
with open('test_long_function.py') as f:
    code = f.read()

max_length = 10
long_functions = longfunctions.find_long_functions(code, max_length)
for func_name, start_line, end_line, length in long_functions:
    print(f"Long function: Function '{func_name}' from line {start_line} to {end_line} ({length} lines) is too long.")

#detect_repeated_functions_with_lines
with open('test_repeated_code.py') as f:
    code = f.read()

repeated_functions_with_lines = repeatedcodesegment.detect_repeated_functions_with_lines(code)
for func_group in repeated_functions_with_lines:
    print("Repeated function(s):")
    for start_line, end_line, func_name in func_group:
        print(f"Repeated function: Function '{func_name}' from line {start_line} to line {end_line}")

#find_unused_variables_and_imports
with open('test_unused_code.py') as f:
    code = f.read()

unused_vars, unused_imports = unusedimport.find_unused_variables_and_imports(code)
print("Unused variables:", unused_vars)
print("Unused imports:", unused_imports)
