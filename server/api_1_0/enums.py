import enum

class RoleEnum(enum.Enum):
    """
    User rolES
    """

    ADMIN = "user:admin"
    USER = "user:self"
    GUEST = "user:guest"
