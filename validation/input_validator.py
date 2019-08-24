from pyguardian.validation.pyguardian_exceptions import *


class InputValidator:

    VALID_PLATFORMS = ["xbox", "playstation", "pc"]
    RESERVED_CHARS = ";/?:@&"
    UNSAFE_CHARS = "<>%{}|\\^~[]`"

    @staticmethod
    def validate(player, platform) -> bool:

        return all((InputValidator.validate_player_str(player, platform),
                    InputValidator.validate_platform_is_valid_platform(platform),
                    InputValidator.validate_platform_is_not_digits(platform)))

    @staticmethod
    def validate_player_str(player, platform) -> bool:
        if player[0].isdigit() and platform.lower().strip() in "xboxplaystation":
            raise PlayerException("Invalid PSN/Xbox ID")

        for char in InputValidator.UNSAFE_CHARS + InputValidator.RESERVED_CHARS:
            if char in player:
                raise PlayerException(f"Disallowed character '{char}'")

        return True

    @staticmethod
    def validate_platform_is_valid_platform(platform) -> bool:
        if platform.lower().strip() not in InputValidator.VALID_PLATFORMS:
            raise PlatformException(f"Not a valid platform '{platform}'")

        return True

    @staticmethod
    def validate_platform_is_not_digits(platform) -> bool:
        if all(char.isdigit() for char in platform):
            raise PlatformException("Platform must be String")

        return True
