import sqlite3
from datetime import date


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


    def get_ports(self):
        from port import Port

        con = sqlite3.connect("shipments.db")  # Connect to the database
        cur = con.cursor()  # Cursor to interact with the database

        # Query to get origin port details
        cur.execute("""SELECT * FROM ports
                    WHERE id = ?""", (self.origin,))
        origin_port_data = cur.fetchone()
        if origin_port_data:
            origin_port = Port(origin_port_data[0], origin_port_data[1], origin_port_data[2], origin_port_data[3], 
                           origin_port_data[4], origin_port_data[5])
        else:
            None

        # Query to get destination port details
        cur.execute("""SELECT * FROM ports
                    WHERE id = ?""", (self.destination,))
        destination_port_data = cur.fetchone()
        if destination_port_data:
            destination_port = Port(destination_port_data[0], destination_port_data[1], destination_port_data[2], 
                                    destination_port_data[3], destination_port_data[4], destination_port_data[5])
        else:
            None

        con.close()  # Close the connection to the database
        return{"origin": origin_port, "destination": destination_port}


    def get_vessel(self):
        from vessel import Vessel

        con = sqlite3.connect("shipments.db")  # Connect to the database
        cur = con.cursor()  # Cursor to interact with the database

        cur.execute("""SELECT * FROM vessels 
                    WHERE imo = ?""", (self.vessel,))
        vessel_data = cur.fetchone()
        if vessel_data:
            vessel = Vessel(vessel_data[0], vessel_data[1], vessel_data[2], vessel_data[3], vessel_data[4], 
                            vessel_data[5], vessel_data[6], vessel_data[7], vessel_data[8], vessel_data[9])
        else:
            vessel = None

        con.close()  # Close the connection to the database
        return vessel


    def calculate_fuel_costs(self, price_per_liter):
        vessel = self.get_vessel()  # Get the vessel object
        if not vessel:
            raise ValueError("Vessel not found")

        fuel_consumption = vessel.get_fuel_consumption(self.distance_naut)  # Fuel consumption for given distance
        total_fuel_used = fuel_consumption * self.duration_hours  # Total fuel used

        total_price = total_fuel_used * price_per_liter  # Calculate total price
        return round(total_price, 3)  # Return the total price rounded up by 3 decimals


    def convert_speed(self, to_format):
        conversion_options = {
            "Knts": 1,
            "Mph": 1.15078,
            "Kmph": 1.852
        }

        if to_format not in conversion_options:
            raise ValueError("Unsupported format")

        return round(self.average_speed * conversion_options[to_format], 6)


    def convert_distance(self, to_format):
        conversion_options = {
            "NM": 1,
            "M": 1852,
            "KM": 1.852,
            "MI": 1.15078,
            "YD": 2025.37
        }

        if to_format not in conversion_options:
            raise ValueError("Unsupported format")
        return round(self.distance_naut * conversion_options[to_format], 6)

    def convert_duration(self, to_format):
        total_minutes = self.duration_hours * 60
        total_seconds = total_minutes * 60

        days = total_minutes // (24 * 60)
        hours = (total_minutes % (24 * 60)) // 60
        minutes = total_minutes % 60

        formatting = {
            "%D": f"{int(days)}",
            "%H": f"{int(self.duration_hours)}",
            "%M": f"{int(total_minutes)}",
            "%D:%H": f"{int(days)}:{int(hours)}",
        }

        if to_format not in formatting:
            raise ValueError("Unsupported format")

        return formatting[to_format]


    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))


shipment = Shipment("78067E7F-D833-4312-A805-C1355F51F065", date(2023, 1, 1), 15649, 5879.249, 864.595, 6.8, "MYTPP", "TRGEM", 9913547)
# print(shipment)
# print(shipment.get_ports())
# print(shipment.get_vessel())
# print(shipment.calculate_fuel_costs(1))
# print(shipment.convert_duration("%D"))
# print(shipment.convert_duration("%H"))
# print(shipment.convert_duration("%M"))
# print(shipment.convert_duration("%D:%H"))
# print(shipment.convert_distance("NM"))
# print(shipment.convert_distance("M"))
# print(shipment.convert_distance("KM"))
# print(shipment.convert_distance("MI"))
# print(shipment.convert_distance("YD"))
# print(shipment.convert_distance("A"))
# print(shipment.convert_speed("Knts"))
# print(shipment.convert_speed("Mph"))
# print(shipment.convert_speed("Kmph"))
# print(shipment.calculate_fuel_costs(1500))
# print(shipment.get_ports())
