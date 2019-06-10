#!/usr/bin/env python3.7
from pyguardian import PyGuardian
from InputValidator import InputValidator
from GuardianProcessor import GuardianProcessor

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
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_stats(guardian, platform))
    if args.response == "eq":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_eq(guardian, platform))
    if args.response == "vault":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_vault(guardian, platform))
    if args.response == "vault-name":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_vault(guardian, platform, sort="name"))
    if args.response == "vault-type":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_vault(guardian, platform, sort="type"))
    if args.response == "vault-tier":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_vault(guardian, platform, sort="tier"))
    if args.response == "playtime":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_playtime(guardian, platform))
    if args.response == "last":
        InputValidator.validate(args.guardian, args.platform)
        guardian, platform = GuardianProcessor.process(args.guardian, args.platform)
        print(PyGuardian.fetch_last_time_played(guardian, platform))
    if args.download_manifest:
        get_manifest.main(url_check=True)
    else:
        pass


if __name__ == "__main__":
    main()
