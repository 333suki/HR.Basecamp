import csv
import os
import sys

from vessel import Vessel
from port import Port
from shipment import Shipment
from datetime import date

import sqlite3
import csv


class Reporter:
    def __init__(self):
        self.con = sqlite3.connect("shipments.db")

    def __del__(self):
        self.con.close()

    # How many vessels are there? -> int
    def total_amount_of_vessels(self) -> int:
        return self.con.execute("""SELECT COUNT(*) FROM vessels""").fetchone()[0]

    # What is the longest shipment distance? -> Shipment
    def longest_shipment(self) -> Shipment:
        query_results = self.con.execute("""SELECT * FROM shipments ORDER BY distance_naut DESC""").fetchone()
        if not query_results:
            return None
        return Shipment(*query_results)

    # What is the longest and shortest vessel? -> tuple[Vessel, Vessel]
    def longest_and_shortest_vessels(self) -> tuple[Vessel, Vessel]:
        query_results = self.con.execute("""SELECT * FROM vessels ORDER BY length, imo DESC""").fetchall()
        shortest = Vessel(*query_results[0])
        longest = Vessel(*query_results[-1])
        return (longest, shortest)

    # What is the widest and smallest vessel? -> tuple[Vessel, Vessel]
    def widest_and_smallest_vessels(self) -> tuple[Vessel, Vessel]:
        query_results = self.con.execute("""SELECT * FROM vessels ORDER BY beam, imo DESC""").fetchall()
        smallest = Vessel(*query_results[0])
        widest = Vessel(*query_results[-1])
        return (widest, smallest)


    # Which vessels have the most shipments -> tuple[Vessel, ...]
    def vessels_with_the_most_shipments(self) -> tuple[Vessel, ...]:
        query_results = self.con.execute("""SELECT vessel FROM shipments""").fetchall()
        vessel_count = {}  # Dict to store the IDs as keys and the amount of times it occured as values
        highest_shipments = []
        vessel_obj = []

        for vessel in query_results:
            if vessel[0] in vessel_count:
                vessel_count[vessel[0]] += 1
            else:
                vessel_count[vessel[0]] = 1

        highest_value = max(vessel_count.values())
        for vessel_id, shipment_count in vessel_count.items():
            if highest_value == shipment_count:
                highest_shipments.append(vessel_id)

        for item in highest_shipments:  # Get the vessel details and create a Vessel object
            query = """SELECT * FROM vessels
                        WHERE imo = ? LIMIT 1"""
            query_results = self.con.execute(query, [item]).fetchone()
            vessel_obj.append(Vessel(*query_results))

        return tuple(vessel_obj)

    # Which ports have the most shipments -> tuple[Port, ...]
    def ports_with_most_shipments(self) -> tuple[Port, ...]:
        query_results = self.con.execute("""SELECT origin, destination FROM shipments""").fetchall()
        port_count = {}
        highest_shipments = []
        port_obj = []

        for origin, destination in query_results:
            if origin in port_count:
                port_count[origin] += 1
            else:
                port_count[origin] = 1

            if destination in port_count:
                port_count[destination] += 1
            else:
                port_count[destination] = 1

            highest_value = max(port_count.values())

        for port_id, shipment_count in port_count.items():  # Find the ports with the highest shipment count
            if highest_value == shipment_count:
                highest_shipments.append(port_id)

        for item in highest_shipments:  # Get the port details and create a Port object
            query = """SELECT * FROM ports WHERE id = ? LIMIT 1"""
            query_results = self.con.execute(query, [item]).fetchone()
            port_obj.append(Port(*query_results))

        return tuple(port_obj)


    # Which ports (origin) had the first shipment? -> tuple[Port, ...]:
    # Which ports (origin) had the first shipment of a specific vessel type?  -> tuple[Port, ...]:
    def ports_with_first_shipment(self, vessel_type: str = None) -> tuple[Port, ...]:
        ports = []
        port_ids = []
        first_date = None

        try:
            if vessel_type is None:  # Get the first shipment date
                first_date = self.con.execute("""SELECT date FROM shipments ORDER BY date LIMIT 1""").fetchone()[0]
            else:
                dates = set(result[0] for result in self.con.execute("""SELECT date FROM shipments ORDER BY date""").fetchall())
                for _date in sorted(dates):
                    vessel_imos = [result[0] for result in self.con.execute("""SELECT vessel FROM shipments
                                                                            WHERE date = ?""", [_date]).fetchall()]
                    for vessel_imo in vessel_imos:
                        db_vessel_type = self.con.execute("""SELECT type FROM vessels
                                                        WHERE imo = ? LIMIT 1""", [vessel_imo]).fetchone()
                        if db_vessel_type[0] == vessel_type:
                            first_date = _date
                            break
                    if first_date:
                        break

            if vessel_type is None:  # Get port IDs for the first shipment date
                query_results = self.con.execute("""SELECT origin FROM shipments
                                                WHERE date = ? ORDER BY origin""", [first_date]).fetchall()
                for result in query_results:
                    port_ids.append(result[0])
            else:
                query_results = self.con.execute("""SELECT origin, vessel FROM shipments
                                                WHERE date = ? ORDER BY origin""", [first_date]).fetchall()
                for origin, vessel in query_results:
                    db_vessel_type = self.con.execute("""SELECT type FROM vessels
                                                    WHERE imo = ? LIMIT 1""", [vessel]).fetchone()
                    if db_vessel_type[0] == vessel_type:
                        port_ids.append(origin)

            for port_id in port_ids:  # Get port details and create Port objects
                query_result = self.con.execute("""SELECT * FROM ports
                                                WHERE id = ? LIMIT 1""", [port_id]).fetchone()
                ports.append(Port(*query_result))

            return tuple(ports)
        except IndexError:
            return None

    # Which ports (origin) had the latest shipment? -> tuple[Port, ...]:
    # Which ports (origin) had the latetst shipment of a specific vessel type? -> tuple[Port, ...]:
    def ports_with_latest_shipment(self, vessel_type: str = None) -> tuple[Port, ...]:
        ports = []
        port_ids = []
        latest_date = None

        try:
            if vessel_type is None:  # Get the latest shipment date
                latest_date = self.con.execute("""SELECT date FROM shipments ORDER BY date DESC LIMIT 1""").fetchone()[0]
            else:
                dates = set(result[0] for result in self.con.execute("""SELECT date FROM shipments ORDER BY date DESC""").fetchall())
                for _date in sorted(dates, reverse=True):
                    vessel_imos = [result[0] for result in self.con.execute("""SELECT vessel FROM shipments WHERE date = ?""", [_date]).fetchall()]
                    for vessel_imo in vessel_imos:
                        db_vessel_type = self.con.execute("""SELECT type FROM vessels
                                                        WHERE imo = ? LIMIT 1""", [vessel_imo]).fetchone()
                        if db_vessel_type[0] == vessel_type:
                            latest_date = _date
                            break
                    if latest_date:
                        break

            if vessel_type is None:  # Get port IDs for the latest shipment date
                query_results = self.con.execute("""SELECT origin FROM shipments
                                                WHERE date = ? ORDER BY origin""", [latest_date]).fetchall()
                for result in query_results:
                    port_ids.append(result[0])
            else:
                query_results = self.con.execute("""SELECT origin, vessel FROM shipments
                                                WHERE date = ? ORDER BY origin""", [latest_date]).fetchall()
                for origin, vessel in query_results:
                    db_vessel_type = self.con.execute("""SELECT type FROM vessels
                                                    WHERE imo = ? LIMIT 1""", [vessel]).fetchone()
                    if db_vessel_type[0] == vessel_type:
                        port_ids.append(origin)

            for port_id in port_ids:  # Get port details and create Port objects
                query_result = self.con.execute("""SELECT * FROM ports
                                                WHERE id = ? LIMIT 1""", [port_id]).fetchone()
                ports.append(Port(*query_result))

            return tuple(ports)
        except IndexError:
            return None

    # Which vessels have docked port Z between period X and Y? -> tuple[Vessel, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Vessels docking Port Z between X and Y.csv`
    # example: `Vessels docking Port MZPOL between 2023-03-01 and 2023-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Vessels, ...)
    # CSV example (this are also the headers):
    #   imo, mmsi, name, country, type, build, gross, netto, length, beam
    def vessels_that_docked_port_between(self, port: Port, start: date, end: date, to_csv: bool = False) -> tuple[Vessel, ...] | None:
        vessels = []
        vessel_ids = []

        query_results = self.con.execute(
            """SELECT vessel FROM shipments
            WHERE (origin = ? OR destination = ?) AND date BETWEEN ? AND ?
            ORDER BY vessel""",
            [port.id, port.id, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")]
        ).fetchall()

        for result in query_results:
            vessel_ids.append(result[0])

        for vessel_id in vessel_ids:
            query_result = self.con.execute(
                """SELECT * FROM vessels
                WHERE imo = ? LIMIT 1""",[vessel_id]).fetchone()
            vessels.append(Vessel(*query_result))

        vessels = tuple(dict.fromkeys(vessels))

        if not to_csv:
            return vessels
        else:
            to_write = [["imo", "mmsi", "name", "country", "type", "build", "gross", "netto", "length", "beam"]]
            for vessel in vessels:
                to_write.append([
                    vessel.imo, vessel.mmsi, vessel.name, vessel.country,
                    vessel.type, vessel.build, vessel.gross, vessel.netto,
                    vessel.length, vessel.beam
                ])

            filename = f"Vessels docking Port {port.id} between {start.strftime('%Y-%m-%d')} and {end.strftime('%Y-%m-%d')}.csv"
            file = open(filename, "wt", newline="", encoding="utf-8")
            writer = csv.writer(file, delimiter=",")
            writer.writerows(to_write)
            file.close()

            return None


    # Which ports are located in country X? ->tuple[Port, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Ports in country X.csv`
    # example: `Ports in country Norway.csv`
    # otherwise it should just return the value as tuple(Port, ...)
    # CSV example (this are also the headers):
    #   id, code, name, city, province, country
    def ports_in_country(self, country: str, to_csv: bool = False) -> tuple[Port, ...] | None:
        ports = []
        query_results = self.con.execute("""SELECT * FROM ports
                                         WHERE country = ? ORDER BY id""",[country]).fetchall()

        for result in query_results:
            ports.append(Port(*result))

        ports = tuple(dict.fromkeys(ports))

        if not to_csv:
            return ports
        else:
            to_write = [["id", "code", "name", "city", "province", "country"]]
            for port in ports:
                to_write.append([
                    port.id, port.code, port.name, port.city,
                    port.province, port.country
                ])

            filename = f"Ports in country {country}.csv"
            file = open(filename, "wt", newline="", encoding="utf-8")
            writer = csv.writer(file, delimiter=",")
            writer.writerows(to_write)
            file.close()

            return None


    # Which vessels are from country X? -> tuple[Vessel, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Vessels from country X.csv`
    # example: `Vessels from country GER.csv`
    # otherwise it should just return the value as tuple(Vessel, ...)
    # CSV example (this are also the headers):
    #   imo, mmsi, name, country, type, build, gross, netto, length, beam
    def vessels_from_country(self, country: str, to_csv: bool = False) -> tuple[Vessel, ...] | None:
        vessels = []
        query_results = self.con.execute("""SELECT * FROM vessels
                                         WHERE country = ?""",[country]).fetchall()

        for result in query_results:
            vessels.append(Vessel(*result))

        vessels = tuple(dict.fromkeys(vessels))

        if not to_csv:
            return vessels
        else:
            to_write = [["imo", "mmsi", "name", "country", "type", "build", "gross", "netto", "length", "beam"]]
            for vessel in vessels:
                to_write.append([
                    vessel.imo, vessel.mmsi, vessel.name, vessel.country,
                    vessel.type, vessel.build, vessel.gross, vessel.netto,
                    vessel.length, vessel.beam
                ])

            filename = f"Vessels from country {country}.csv"
            file = open(filename, "wt", newline="", encoding="utf-8")
            writer = csv.writer(file, delimiter=",")
            writer.writerows(to_write)
            file.close()

            return None


reporter = Reporter()
# print(reporter.total_amount_of_vessels())
# print(reporter.longest_shipment())
# print(reporter.vessels_with_the_most_shipments())
# print(reporter.ports_with_most_shipments())
# print(reporter.longest_and_shortest_vessels())
# print(reporter.ports_with_first_shipment())
