class PlayerException(Exception):
    pass


class PlatformException(Exception):
    pass


class APIException(Exception):
    pass


class PlayerNotFoundException(Exception):
    pass


class CannotCreateStorageDirectories(Exception):
    pass


class VaultAccessBlockedException(Exception):
    pass


class NoPlayerEquipmentException(Exception):
    pass


class APIUnavailableException(Exception):
    pass
