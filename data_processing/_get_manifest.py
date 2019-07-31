"""
This will be the class-structure version of the get_manifest script
"""
from time import sleep
from ..utils import constants
import requests
import shutil
import sqlite3
import json
import zipfile
import sys
import os


class GetManifest:

    def __call__(self):
        pass

    @staticmethod
    def _check_dirs(self):
        """
        Just checks that the directories used for reading and
        storage exist, creates otherwise

        :return: None
        """
        try:
            if not os.path.isdir(constants.DATA_DIR):
                print("Creating data directory")
                os.makedirs(constants.MANIFEST_DIR)
            if not os.path.isdir(constants.MANIFEST_DIR):
                print("Creating manifest directory")
                os.makedirs(constants.MANIFEST_DIR)
            if not os.path.isdir(constants.JSON_DIR):
                print("Creating JSON directory")
                os.makedirs(constants.JSON_DIR)
        except OSError:
            print("Can't create directories!")
            sys.exit()

    def _check_manifest_uri(self, uri):
        pass

    def _get_manifest_url(self):
        pass

    def _get_manifest(self):
        pass

    def _unzip_and_rename(self):
        pass

    def _write_tables(self):
        pass
