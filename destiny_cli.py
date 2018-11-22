#!/usr/bin/env python3.7
from pyguardian import PyGuardian
import get_manifest
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("guardian", nargs="?", action="store", default=None)
    parser.add_argument("platform", nargs="?", action="store", default=None)
    parser.add_argument("response", nargs="?", action="store", default=None)
    parser.add_argument("-d", "--download", action="store_true")

    args = parser.parse_args()

    if args.response == "stats":
        print(PyGuardian.fetch_stats(args.guardian, args.platform))
    if args.response == "eq":
        print(PyGuardian.fetch_eq(args.guardian, args.platform))
    if args.response == "vault":
        print(PyGuardian.fetch_vault(args.guardian, args.platform))
    if args.response == "playtime":
        print(PyGuardian.fetch_playtime(args.guardian, args.platform))
    if args.response == "last":
        print(PyGuardian.fetch_last_played(args.guardian, args.platform))
    if args.download:
        get_manifest.main()
    else:
        pass


if __name__ == "__main__":
    main()
