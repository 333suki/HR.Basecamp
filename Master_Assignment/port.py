import sqlite3

class Port:

    def __init__(self, id: str, code: int, name: str, city: str, province: str, country: str) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.city = city
        self.province = province
        self.country = country

    def get_shipments(self):  # Returns a tuple of Shipments for this port (can be origin or destination)
        from shipment import Shipment  # Import the Shipment class

        con = sqlite3.connect("shipments.db")  # Connect to the database
        cur = con.cursor()  # Cursor to interact with the database
        shipments = []  # Empty list to store the shipments

        query = """
        SELECT * FROM shipments
        WHERE origin = ? OR destination = ?
        """  # Database query to select shipments where the port is origin or destination

        cur.execute(query, [self.id, self.id])  # Execute the query
        query_results = cur.fetchall()  # Fetch all (remaining) rows of query and return a list of tuples
        for result in query_results:
            shipments.append(Shipment(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                      result[7], result[8]))

        con.close()  # Close the connection
        return tuple(shipments)

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))

port = Port("MYTPP", 55750, "Tajung Pelepas", "Tanjung Pelepas", "Johor", "Malaysia")
shipments = port.get_shipments()
# print(shipments)
