class Shipment:

    def __init__(self, id, date, cargo_weight, distance_naut, duration_hours, average_speed, origin, destination, vessel) -> None:
        self.id = id
        self.date = date
        self.cargo_weight = cargo_weight
        self.distance_naut = distance_naut
        self.duration_hours = duration_hours
        self.average_speed = average_speed
        self.origin = origin
        self.destination = destination
        self.vessel = vessel

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
