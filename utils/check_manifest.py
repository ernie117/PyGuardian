import requests

from pyguardian.utils import constants
from pyguardian.validation.PyGuardian_Exceptions import APIUnavailableException


class CheckManifest:

    def __call__(self):
        check_uri = self._get_manifest_url()
        return_uri = self._check_manifest_uri(check_uri)

        return return_uri

    @staticmethod
    def _get_manifest_url():
        """
        Requests an URL for the manifest SQL data
        """
        r = requests.get(constants.MANIFEST_URL,
                         headers=constants.HEADERS).json()

        if r["ErrorStatus"] == "SystemDisabled":
            raise APIUnavailableException("API is down!")

        return r["Response"]["mobileWorldContentPaths"]["en"]

    @staticmethod
    def _check_manifest_uri(uri):
        try:
            with open(constants.MANIFEST_CHECK_FILE, 'r+') as f:
                check_url = f.read().strip()

                if uri == check_url:
                    return None

                f.seek(0)
                f.write(uri)

        except FileNotFoundError:
            print("Creating manifest url check-file")
            with open(constants.MANIFEST_CHECK_FILE, 'w') as f:
                f.write(uri)

        return uri
