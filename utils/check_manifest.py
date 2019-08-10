import os

import requests

from pyguardian.utils import constants
from pyguardian.utils.pyguardian_decorators import log_me
from pyguardian.utils.pyguardian_logging import PyGuardianLogger
from pyguardian.validation.pyguardian_exceptions import APIUnavailableException


class CheckManifest:
    LOGGER = PyGuardianLogger(os.path.basename(os.path.realpath(__file__)))

    def __call__(self):
        check_uri = self._get_manifest_uri()
        return_uri = self._check_manifest_uri(check_uri)

        return return_uri

    @staticmethod
    @log_me
    def _get_manifest_uri():
        """
        Requests an URI for the manifest SQL data, changes
        when manifest is updated, so can be used to determine
        when to re-download manifest data

        :return: URI from which to download manifest data
        """
        r = requests.get(constants.MANIFEST_URL,
                         headers=constants.HEADERS).json()

        if r["ErrorStatus"] == "SystemDisabled":
            CheckManifest.LOGGER.warn("Bungie API is down")
            raise APIUnavailableException("API is down!")

        return r["Response"]["mobileWorldContentPaths"]["en"]

    @staticmethod
    @log_me
    def _check_manifest_uri(uri):
        """
        Checks retrieved manifest URI against one recorded on
        file, if it's changed there is new data to download

        :param uri: URI to check
        :return: None if URI is the same, returns new URI
        otherwise
        """
        if os.path.isfile(constants.MANIFEST_CHECK_FILE):
            with open(constants.MANIFEST_CHECK_FILE, 'r+') as f:
                check_url = f.read().strip()

                if uri == check_url:
                    return None

                f.seek(0)
                f.write(uri)

        else:
            CheckManifest.LOGGER.warn("Creating manifest url check-file...")
            with open(constants.MANIFEST_CHECK_FILE, 'w') as f:
                f.write(uri)

        return uri
