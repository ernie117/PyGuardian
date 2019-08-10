import json
import os


class MockManifestSuccessfulResponse:

    def __init__(self):
        self.response_data = {
            "ErrorStatus": "Active",
            "Response": {
                "mobileWorldContentPaths": {
                    "en": "/made-up-URL"
                }
            }
        }

    def json(self):
        return self.response_data


class MockManifestSuccessfulResponseNewURI:

    def __init__(self):
        self.response_data = {
            "ErrorStatus": "Active",
            "Response": {
                "mobileWorldContentPaths": {
                    "en": "/shiny-new-uri"
                }
            }
        }

    def json(self):
        return self.response_data


class MockManifestUnsuccessfulResponse:

    def __init__(self):
        self.response_data = {
            "ErrorStatus": "SystemDisabled"
        }

    def json(self):
        return self.response_data


class MockSearchDestinyPlayerSuccessfulResponse:

    def __init__(self):
        self.response_data = {
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

    def json(self):
        return self.response_data


class MockSearchDestinyPlayerUnsuccessfulResponse:

    def __init__(self):
        self.response_data = {
            "ErrorStatus": "SystemDisabled"
        }

    def json(self):
        return self.response_data


class MockSearchDestinyPlayerNoSuchPlayer:

    def __init__(self):
        self.response_data = {
            "Response": [],
            "ErrorCode": 1,
            "ThrottleSeconds": 0,
            "ErrorStatus": "Success",
            "Message": "Ok",
            "MessageData": {}
        }

    def json(self):
        return self.response_data


class MockSuccessfulCharacterDataRequest:

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_character_data.json", "r") as f:
            self.response_data = json.load(f)

    def json(self):
        return self.response_data


class MockUnsuccessfulCharacterDataRequest:

    def __init__(self):
        self.response_data = {
            "Response": [],
            "ErrorCode": 1,
            "ThrottleSeconds": 0,
            "ErrorStatus": "Success",
            "Message": "Ok",
            "MessageData": {}
        }

    def json(self):
        return self.response_data


class MockSuccessfulCharacterEquipmentDataRequest:

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_equip_data.json", "r") as f:
            self.response_data = json.load(f)

    def json(self):
        return self.response_data


class MockSuccessfulVaultDataRequest:

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  "/dummy_vault_data.json", "r") as f:
            self.response_data = json.load(f)

    def json(self):
        return self.response_data
