class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({}, {})".format(
            self.type,
            self.value
        )

    def __repr__(self):
        self.__str__()
