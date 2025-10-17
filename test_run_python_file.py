#!/usr/bin/env python3

from functions.run_python_file import run_python_file

print("=== Test 1: Calculator usage instructions ===")
result = run_python_file("calculator", "main.py")
print(result)

print("\n=== Test 2: Calculator with expression ===")
result = run_python_file("calculator", "main.py", ["3 + 5"])
print(result)

print("\n=== Test 3: Run calculator tests ===")
result = run_python_file("calculator", "test.py")
print(result)

print("\n=== Test 4: Outside working directory ===")
result = run_python_file("calculator", "../main.py")
print(result)

print("\n=== Test 5: Nonexistent file ===")
result = run_python_file("calculator", "nonexistent.py")
print(result)

print("\n=== Test 6: Not a Python file ===")
result = run_python_file("calculator", "lorem.txt")
print(result)
