#!/usr/bin/env python3.7
import argparse
import logging
import os
import sys

from pyguardian.data_processing.get_manifest import GetManifest
from pyguardian.main.pyguardian import PyGuardian
from pyguardian.utils.check_manifest import CheckManifest
from pyguardian.utils.pyguardian_logging import PyGuardianLogger


def create_parser():
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
    parser.add_argument("-l", "--log", action="store_true")

    return parser


def main(cli_args):
    parser = create_parser()
    args = parser.parse_args(cli_args)

    log = PyGuardianLogger(name=os.path.basename(__file__))
    # disable logging as default
    logging.disable()
    if args.log:
        logging.disable(logging.NOTSET)

    if args.response == "stats":
        print(PyGuardian.fetch_stats(args.guardian, args.platform, log))
    elif args.response == "eq":
        print(PyGuardian.fetch_eq(args.guardian, args.platform, log))
    elif args.response == "vault":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, log))
    elif args.response == "vault-name":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, log, sort="name"))
    elif args.response == "vault-type":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, log, sort="type"))
    elif args.response == "vault-tier":
        print(PyGuardian.fetch_vault(args.guardian, args.platform, log, sort="tier"))
    elif args.response == "playtime":
        print(PyGuardian.fetch_playtime(args.guardian, args.platform, log))
    elif args.response == "last":
        print(PyGuardian.fetch_last_time_played(args.guardian, args.platform, log))
    elif args.download_manifest:
        check_manifest = CheckManifest()
        uri = check_manifest()
        get_manifest = GetManifest()
        get_manifest(uri)


if __name__ == "__main__":
    main(sys.argv[1:])
