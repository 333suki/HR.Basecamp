import sqlite3

class Vessel:

    def __init__(self, imo: int, mmsi: int, name: str, country: str, type: str, build: int, gross: int, netto: int, length: int, beam: int) -> None:
        self.imo = imo
        self.mmsi = mmsi
        self.name = name
        self.country = country
        self.type = type
        self.build = build
        self.gross = gross
        self.netto = netto
        self.length = length
        self.beam = beam


    def get_shipments(self): # Returns a tuple of Shipments for this vessel
        from shipment import Shipment

        con = sqlite3.connect("shipments.db")
        cur = con.cursor()
        shipments = []

        query = """
        SELECT * FROM shipments
        WHERE vessel = ?
        """

        cur.execute(query, [self.imo])
        results = cur.fetchall()
        for result in results:
            shipments.append(Shipment(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], 
                                      result[8]))

        con.close()
        return tuple(shipments)


    def get_fuel_consumption(self, distance): # Returns a number based on calculations
        ship_types = {
            "Aggregates Carrier": 0.4,
            "Bulk Carrier": 0.35,
            "Oil Carrier": 0.35,
            "Cement Carrier": 0.4,
            "Container Ship": 0.3,
            "Deck Cargo Ship": 0.4,
            "General Cargo Ship": 0.4,
            "Heavy Load Carrier": 0.4,
            "Landing Craft": 0.4,
            "Nuclear Fuel Carrier": 0.35,
            "Palletised Cargo Ship": 0.4,
            "Passenger": 0.3,
            "Ro-Ro Cargo Ship": 0.4,
            "Self Discharging Bulk Carrier": 0.35,
            "Vehicles Carrier": 0.35,
            "Wood Chips Carrier": 0.4
        }

        efficiency = ship_types.get(self.type, 0)
        fuel = efficiency * (self.gross / self.netto) * distance
        fuel = round(fuel, 5)

        return fuel

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))

vessel = Vessel(1034034, None, "GREAT WALL 17", "Tanzania", "Deck Cargo Ship", 2023, 1978, 2373, 84, 19)
print(vessel.get_shipments)
print(vessel.get_fuel_consumption(1500))
