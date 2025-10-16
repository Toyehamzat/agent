#!/usr/bin/env python3

from functions.write_file import write_file
import os

def test_write_file():
    # Test 1: Write a simple file in calculator directory
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"Test 1 - Write lorem.txt: {result}")
    
    # Test 2: Write to a subdirectory in calculator
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"Test 2 - Write to pkg/morelorem.txt: {result}")
    
    # Test 3: Try to write to absolute path (should not be allowed)
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"Test 3 - Write to /tmp/temp.txt: {result}")
    
    # # Cleanup
    # try:
    #     if os.path.exists("calculator/lorem.txt"):
    #         os.remove("calculator/lorem.txt")
    #     if os.path.exists("calculator/pkg/morelorem.txt"):
    #         os.remove("calculator/pkg/morelorem.txt")
    #     if os.path.exists("calculator/pkg"):
    #         os.rmdir("calculator/pkg")
    #     print("Cleanup completed")
    # except Exception as e:
    #     print(f"Cleanup error: {e}")

if __name__ == "__main__":
    test_write_file()