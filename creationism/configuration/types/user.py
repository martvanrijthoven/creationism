class UserObject:
    def __init__(self, config_value):
        self.data = config_value


class UserInt(UserObject):
    ...


class UserFloat(UserObject):
    ...


class UserBool(UserObject):
    ...


class UserInstance(UserObject):
    ...


class UserNone(UserObject):
    ...