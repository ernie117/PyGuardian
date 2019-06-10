#!/usr/bin/env python3.7
from main.pyguardian import PyGuardian
from validation.InputValidator import InputValidator
from validation.GuardianProcessor import GuardianProcessor

from data_processing import get_manifest
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

    # TODO maybe offload this to the PyGuardian class
    raw_guardian, raw_platform = args.guardian, args.platform
    InputValidator.validate(raw_guardian, raw_platform)
    final_guardian, final_platform = GuardianProcessor.process(raw_guardian, raw_platform)

    if args.response == "stats":
        print(PyGuardian.fetch_stats(final_guardian, final_platform))
    elif args.response == "eq":
        print(PyGuardian.fetch_eq(final_guardian, final_platform))
    elif args.response == "vault":
        print(PyGuardian.fetch_vault(final_guardian, final_platform))
    elif args.response == "vault-name":
        print(PyGuardian.fetch_vault(final_guardian, final_platform, sort="name"))
    elif args.response == "vault-type":
        print(PyGuardian.fetch_vault(final_guardian, final_platform, sort="type"))
    elif args.response == "vault-tier":
        print(PyGuardian.fetch_vault(final_guardian, final_platform, sort="tier"))
    elif args.response == "playtime":
        print(PyGuardian.fetch_playtime(final_guardian, final_platform))
    elif args.response == "last":
        print(PyGuardian.fetch_last_time_played(final_guardian, final_platform))
    elif args.download_manifest:
        get_manifest.main(url_check=True)
    else:
        pass


if __name__ == "__main__":
    main()
