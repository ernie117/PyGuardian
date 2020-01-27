from pyguardian.validation.pyguardian_exceptions import APIException, \
    APIUnavailableException


class APIStatusChecker:

    def __init__(self, response):

        APIStatusChecker._check_response(response)

    @staticmethod
    def _check_response(response):
        if response["ErrorStatus"] == "SystemDisabled":
            raise APIUnavailableException("API is down!")
        elif response["ErrorStatus"] == "UnhandledException" \
                or response["ErrorStatus"] == "DestinyThrottledByGameServer" \
                or response["ErrorStatus"] == "DestinyShardRelayClientTimeout":
            raise APIException(
                f"API problem: {response['Message']} | {response['ThrottleSeconds']}")
        elif response["ErrorStatus"] == "PerApplicationThrottleExceeded":
            raise APIException(
                f"Getting throttled: {response['Message']} | {response['ThrottleSeconds']}")
