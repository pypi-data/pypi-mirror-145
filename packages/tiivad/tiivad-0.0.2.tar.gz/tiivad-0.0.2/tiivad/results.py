class Results(object):
    __instance = None
    val = []

    def __new__(cls, val):
        if Results.__instance is None:
            Results.__instance = object.__new__(cls)
        if val is not None:
            Results.__instance.val.append(val)
        return Results.__instance

    def clear(cls):
        cls._instance = None


if __name__ == '__main__':
    print(Results({"a", "b"}).val)
    print(Results(None).val)
    print(Results({"a", "b"}).val)
    print(Results(None).val)
    print(Results({"a", "b"}).val)
    print(Results(None).val)
    print(Results({"a", "b"}).val)
    print(Results(None).val)
