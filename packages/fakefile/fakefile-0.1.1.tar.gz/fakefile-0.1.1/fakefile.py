'''
The purpose of this program is to generate a fake file 
of a given size and format. 

The content of the file would be random bytes.
So it won't actually open, and would show up as a corrupt file.

Created by anuvc
'''

import logging
import os
import sys
import argparse

def generate_fakefile(filename, filesize_in_KiB):
    
    filesize_in_bytes = int(1024*filesize_in_KiB)
    
    if filesize_in_bytes <= 0:
        logging.error("filesize too small, defaulting to 1 byte")
        filesize_in_bytes = 1

    with open(filename, 'wb') as fakefile:
        random_bytes = os.urandom(filesize_in_bytes)
        fakefile.write(random_bytes)


def parse_commandline_args():
        """Handles the command line interface using argpase"""
        parser = argparse.ArgumentParser(description="Create a fakefile!, view --help")
        parser.add_argument(
            'filename', 
            type = argparse.FileType('w'),
            nargs = '?', 
            help = 'name of the fakefile, defaults to fakefile.txt'
            )
        parser.add_argument(
            'size',
            type = float,
            nargs = '?',
            help = "size of the fakefile, defaults to 1 KiB"
        )
        args = parser.parse_args()
        if args.filename == None or args.size == None:
            print("ERROR: usage: fakefile [-h] [filename] [size]")
            sys.exit(1)
        return args

def main():
    args = parse_commandline_args()
    generate_fakefile(args.filename.name, args.size)

if __name__ == '__main__':
    main()