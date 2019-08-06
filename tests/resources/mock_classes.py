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
