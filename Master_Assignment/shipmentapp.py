import os
import sys
import json
import sqlite3

from vessel import Vessel
from port import Port
from shipment import Shipment


def read_from_json(filename) -> list:
    with open(os.path.join(sys.path[0], filename), 'r') as file:
        data = json.load(file)
    return data


def json_to_database(): # Function to convert the json to sqlite database
    con = sqlite3.connect("shipments.db") # Open a connection to the database
    cur = con.cursor() # Create a cursor to execute SQL statements
    data = read_from_json("shipments.json") # Open the JSON file

    # Could also use set()
    vessel_id_list = [] # List that keeps track of the existing vessel IDs
    port_id_list = [] # List that keeps track of the existing port IDs
    shipment_id_list = [] # List that keeps track of the existing shipment IDs

    for item in data: # Iterare through the JSON file and insert into database
        if item["vessel"]["imo"] not in vessel_id_list: # Check the ID of the vessel dict
            vessel_id_list.append(item["vessel"]["imo"]) # Add dupe ID to the list
            size = item["vessel"]["size"].split(" / ") # Split the size list into 2 indexes: length and beam
            query_vessel = """ 
                INSERT OR REPLACE INTO vessels
                    (imo, mmsi, name, country, type, build, gross, netto, length, beam)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            # print(item)
            cur.execute(query_vessel, [item["vessel"]["imo"], item["vessel"]["mmsi"], item["vessel"]["name"], 
                                item["vessel"]["country"], item["vessel"]["type"], item["vessel"]["build"], 
                                item["vessel"]["gross"], item["vessel"]["netto"], int(size[0]), int(size[1])])
    
        if item["origin"]["id"] not in port_id_list: # Check the ID of the origin dict
            port_id_list.append(item["origin"]["id"]) # Append into the list if not a dupe
            query_origin = """
                INSERT OR REPLACE INTO ports
                    (id, code, name, city, province, country)
                    VALUES (?, ?, ?, ?, ?, ?)"""
            
            cur.execute(query_origin, [item["origin"]["id"], item["origin"]["code"], item["origin"]["name"], 
                                    item["origin"]["city"], item["origin"]["province"], item["origin"]["country"]])
            
        if item["destination"]["id"] not in port_id_list: # Check the ID of the destination dict
            port_id_list.append(item["destination"]["id"]) # Append into the list if not a dupe
            query_destination = """
                INSERT OR REPLACE INTO ports
                    (id, code, name, city, province, country)
                    VALUES (?, ?, ?, ?, ?, ?)"""
            
            cur.execute(query_destination, [item["destination"]["id"], item["destination"]["code"], 
                                            item["destination"]["name"], item["destination"]["city"], 
                                            item["destination"]["province"], item["destination"]["country"]])

        query_shipment = """
                INSERT OR REPLACE INTO shipments
                (id, date, cargo_weight, distance_naut, duration_hours, average_speed, origin, destination, vessel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cur.execute(query_shipment, [item["tracking_number"], item["date"], item["cargo_weight"], item["distance_naut"],
                                      item["duration_hours"], item["average_speed"], item["origin"]["id"], 
                                      item["destination"]["id"], item["vessel"]["imo"]])

    con.commit() # Commit as late as possible


if __name__ == "__main__":
    try: read_from_json(f"shipments.json")
    except FileNotFoundError:
        print("File not found")
    json_to_database()
