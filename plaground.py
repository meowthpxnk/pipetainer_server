import enum


class Role(enum.Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    SUPPORT = "SUPPORT"

    # def __eq__(self, other):
    #     if not isinstance(other, self.__class__):
    #         raise TypeError("Other must be Role type.")

    #     return self.value == other.value

    # def __ne__(self, other):
    #     if not isinstance(other, self.__class__):
    #         raise TypeError("Other must be Role type.")
    #     return self.value != other.value

    # def __lt__(self, other):
    #     if not isinstance(other, self.__class__):
    #         raise TypeError("Other must be Role type.")

    #     match self.value:
    #         case "ADMIN":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return False
    #             elif other.value == "SUPPORT":
    #                 return False
    #         case "SUPERVISOR":
    #             if other.value == "ADMIN":
    #                 return True
    #             elif other.value == "SUPERVISOR":
    #                 return False
    #             elif other.value == "SUPPORT":
    #                 return True
    #         case "SUPPORT":
    #             if other.value == "ADMIN":
    #                 return True
    #             elif other.value == "SUPERVISOR":
    #                 return True
    #             elif other.value == "SUPPORT":
    #                 return False

    # def __le__(self, other):
    #     if not isinstance(other, self.__class__):
    #         raise TypeError("Other must be Role type.")

    #     match self.value:
    #         case "ADMIN":
    #             if other.value == "ADMIN":
    #                 return True
    #             elif other.value == "SUPERVISOR":
    #                 return False
    #             elif other.value == "SUPPORT":
    #                 return False
    #         case "SUPERVISOR":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return True
    #             elif other.value == "SUPPORT":
    #                 return True
    #         case "SUPPORT":
    #             if other.value == "ADMIN":
    #                 return True
    #             elif other.value == "SUPERVISOR":
    #                 return True
    #             elif other.value == "SUPPORT":
    #                 return True

    # def __gt__(self, other):
    #     if not isinstance(other, self.__class__):
    #         raise TypeError("Other must be Role type.")

    #     match self.value:
    #         case "ADMIN":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return True
    #             elif other.value == "SUPPORT":
    #                 return True
    #         case "SUPERVISOR":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return False
    #             elif other.value == "SUPPORT":
    #                 return True
    #         case "SUPPORT":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return False
    #             elif other.value == "SUPPORT":
    #                 return False

    # def __ge__(self, other):
    #     if not isinstance(other, self.__class__):
    #         raise TypeError("Other must be Role type.")

    #     match self.value:
    #         case "ADMIN":
    #             if other.value == "ADMIN":
    #                 return True
    #             elif other.value == "SUPERVISOR":
    #                 return True
    #             elif other.value == "SUPPORT":
    #                 return True
    #         case "SUPERVISOR":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return True
    #             elif other.value == "SUPPORT":
    #                 return True
    #         case "SUPPORT":
    #             if other.value == "ADMIN":
    #                 return False
    #             elif other.value == "SUPERVISOR":
    #                 return False
    #             elif other.value == "SUPPORT":
    #                 return True


SUPERUSER_USERNAME = "admin"


class User:
    username: str
    role: Role

    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role


superuser = User(SUPERUSER_USERNAME, Role.ADMIN)
admin = User("adm", Role.ADMIN)
admin2 = User("adm", Role.ADMIN)
supervisor = User("super", Role.SUPERVISOR)
supervisor2 = User("super", Role.SUPERVISOR)
support = User("support", Role.SUPPORT)
support2 = User("support", Role.SUPPORT)


# print(support.role < admin2.role)
print(admin.role == Role.ADMIN)
