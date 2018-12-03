#!/usr/bin/env python3.7
from pyguardian import PyGuardian
import get_manifest
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("guardian", type=str, nargs="?", action="store", default=None)
    parser.add_argument("platform", type=str, nargs="?", action="store", default=None,
                        choices=["pc",
                                 "playstation",
                                 "xbox"])
    parser.add_argument("response", type=str, nargs="?", action="store", default=None,
                        choices=["stats",
                                 "eq",
                                 "vault",
                                 "vault-name",
                                 "vault-type",
                                 "vault-tier",
                                 "playtime",
                                 "last"])
    parser.add_argument("-d", "--download-manifest", action="store_true")

    args = parser.parse_args()

    if args.response == "stats":
        print(PyGuardian.fetch_stats(args.guardian, args.platform))
    if args.response == "eq":
        print(PyGuardian.fetch_eq(args.guardian, args.platform))
    if args.response == "vault":
        print(PyGuardian.fetch_vault(args.guardian, args.platform))
    if args.response == "vault-name":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, sort="name"))
    if args.response == "vault-type":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, sort="type"))
    if args.response == "vault-tier":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, sort="tier"))
    if args.response == "playtime":
        print(PyGuardian.fetch_playtime(args.guardian, args.platform))
    if args.response == "last":
        print(PyGuardian.fetch_last_time_played(args.guardian, args.platform))
    if args.download_manifest:
        get_manifest.main()
    else:
        pass


if __name__ == "__main__":
    main()
