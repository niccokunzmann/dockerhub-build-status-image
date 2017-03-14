#!/usr/bin/python3
"""

"""
import sys
import os
from bottle import run, get, static_file

__version__ = "0.0.0"
__author__ = "Nicco Kunzmann"

@get('/source')
def static():
    return static_file(os.path.basename(__file__),
                       root=os.path.dirname(__file__))

def main():
    run(host='', port=80, debug=True)

if __name__ == "__main__":
    main()