class Port:

    def __init__(self, id: str, code: int, name: str, city: str, province: str, country: str) -> None:
        pass

    def get_shipments():
        pass

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
