import json
import os

from pyguardian.tests.resources import test_constants


class BaseMockDataResponse:

    def __init__(self, data):
        self.response_data = data

    def json(self):
        return self.response_data


class MockManifestSuccessfulResponse(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "ErrorStatus": "Active",
                "Response": {
                    "mobileWorldContentPaths": {
                        "en": "/made-up-URL"
                    }
                }
            }
        )


class MockManifestSuccessfulResponseNewURI(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "ErrorStatus": "Active",
                "Response": {
                    "mobileWorldContentPaths": {
                        "en": "/shiny-new-uri"
                    }
                }
            }
        )


class MockManifestUnsuccessfulResponse(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "ErrorStatus": "SystemDisabled"
            }
        )


class MockSearchDestinyPlayerSuccessfulResponse(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "Response": [
                    {
                        "membershipType": 4,
                        "membershipId": "1234567890987654321",
                        "displayName": "ernie"
                    }
                ],
                "ErrorCode": 1,
                "ThrottleSeconds": 0,
                "ErrorStatus": "Success",
                "Message": "Ok",
                "MessageData": {}
            }
        )


class MockSearchDestinyPlayerUnsuccessfulResponse(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "ErrorStatus": "SystemDisabled"
            }
        )


class MockSearchDestinyPlayerNoSuchPlayer(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "Response": [],
                "ErrorCode": 1,
                "ThrottleSeconds": 0,
                "ErrorStatus": "Success",
                "Message": "Ok",
                "MessageData": {}
            }
        )


class MockSuccessfulCharacterDataRequest(BaseMockDataResponse):

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_character_data.json", "r") as f:
            super().__init__(json.load(f))


class MockUnsuccessfulCharacterDataRequest(BaseMockDataResponse):

    def __init__(self):
        super().__init__(
            {
                "Response": [],
                "ErrorCode": 1,
                "ThrottleSeconds": 0,
                "ErrorStatus": "Success",
                "Message": "Ok",
                "MessageData": {}
            }
        )


class MockSuccessfulCharacterEquipmentDataRequest(BaseMockDataResponse):

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_equip_data.json", "r") as f:
            super().__init__(json.load(f))


class MockSuccessfulVaultDataRequest(BaseMockDataResponse):

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_vault_data.json", "r") as f:
            super().__init__(json.load(f))


class MockInventoryDefinition(BaseMockDataResponse):

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_inventoryItemDefinition.json", "r") as f:
            super().__init__(json.load(f))


class MockCheckManifest:

    def __call__(self):
        return True


class MockCheckManifestReturnNone:

    def __call__(self):
        return None


class MockGetManifest:

    def __call__(self, uri):
        return True
