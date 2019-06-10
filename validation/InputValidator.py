from validation.PyGuardian_Exceptions import *


class InputValidator:

    VALID_PLATFORMS = ["xbox", "playstation", "pc"]
    RESERVED_CHARS = ";/?:@&"
    UNSAFE_CHARS = "<>%{}|\\^~[]`"

    @staticmethod
    def validate(player, platform) -> bool:

        return all((InputValidator.validate_player_str(player, platform), 
                   InputValidator.validate_platform_str(platform)))

    @staticmethod
    def validate_player_str(player, platform) -> bool:
        if player[0].isdigit() and platform.lower().strip() in "xboxplaystation":
            raise PlayerException("Invalid PSN/Xbox ID")

        for char in InputValidator.RESERVED_CHARS:
            if char in player:
                raise PlayerException(f"Disallowed character '{char}'")

        for char in InputValidator.UNSAFE_CHARS:
            if char in player:
                raise PlayerException(f"Disallowed character '{char}'")

        return True

    @staticmethod
    def validate_platform_str(platform) -> bool:
        if platform.lower().strip() not in InputValidator.VALID_PLATFORMS:
            raise PlatformException(f"Not a valid platform '{platform}'")

        if all(char.isdigit() for char in platform):
            raise PlayerException("Platform must be String")

        return True
