#!/usr/bin/env python3.7
import sys
from pyguardian.main import destiny_cli


if __name__ == "__main__":
    destiny_cli.main(sys.argv[1:])
