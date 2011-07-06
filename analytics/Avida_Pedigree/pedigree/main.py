#! /Library/Frameworks/Python.framework/Versions/3.1/bin/python3
import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pedigree detail_dump_file_name")
        exit()
    file_name = sys.argv[1]
    pedigree_parsing.create_pedigree_from_detail_file(file_name)
