from vessel import Vessel
from shipment import Shipment
import datetime


# Test to check if duration is converted correctly based on the given arguments
# 1) %D:%H:%M
# 2) %H:%M
def test_convert_duration():
    shipment = Shipment(
            id="78067E7F-D833-4312-A805-C1355F51F065", date=("2023, 1, 1"),
            cargo_weight=15649, distance_naut=5879.249, duration_hours=864.595, average_speed=6.8,
            origin="MYTPP", destination="TRGEM", vessel=9913547)

    assert shipment.convert_duration("%D") == "36"
    assert shipment.convert_duration("%H") == "864"
    assert shipment.convert_duration("%M") == "51875"
    assert shipment.convert_duration("%D:%H") == "36:0"

# Test to check if distance is converted correctly based on the given arguments
# 1) NM = Nautical Meters
# 2) M = Meters
# 3) KM = Kilometers
# 4) MI = Miles
# 5) YD = Yards
# 6) ValueError check
def test_convert_distance():
    shipment = Shipment(
            id="78067E7F-D833-4312-A805-C1355F51F065", date=("2023, 1, 1"),
            cargo_weight=15649, distance_naut=5879.249, duration_hours=864.595, average_speed=6.8,
            origin="MYTPP", destination="TRGEM", vessel=9913547)

    assert shipment.convert_distance("NM") == 5879.249
    assert shipment.convert_distance("M") == 10888369.148
    assert shipment.convert_distance("KM") == 10888.369148
    assert shipment.convert_distance("MI") == 6765.722164
    assert shipment.convert_distance("YD") == 11907654.54713
    try:
        shipment.convert_distance("A")
        assert False
    except ValueError:
        assert True


# Test to check if speed is converted correctly based on the given arguments
# 1) Knts = Knots
# 2) Mph = Miles per hour
# 3) Kph = Kilometers per hour
# 4) ValueError check
def test_convert_speed():
    shipment = Shipment(
        id="78067E7F-D833-4312-A805-C1355F51F065", date=("2023, 1, 1"),
        cargo_weight=15649, distance_naut=5879.249, duration_hours=864.595, average_speed=6.8,
        origin="MYTPP", destination="TRGEM", vessel=9913547)

    assert shipment.convert_speed("Knts") == 6.8
    assert shipment.convert_speed("Mph") == 7.825304
    assert shipment.convert_speed("Kmph") == 12.5936


# Test to check if the fuel consumption is calculated correctly based on the distance
def test_get_fuel_consumption():
    vessel = Vessel(
    1034034, None, "GREAT WALL 17", "Tanzania", "Deck Cargo Ship", 2023, 1978, 2373, 84, 19)

    assert vessel.get_fuel_consumption(1500) == 500.12642

# Test to check if the fuel costs are calculated correctly based on the price per liter
def test_calculate_fuel_costs():
    shipment = Shipment(
        id="78067E7F-D833-4312-A805-C1355F51F065", date=("2023, 1, 1"),
        cargo_weight=15649, distance_naut=5879.249, duration_hours=864.595, average_speed=6.8,
        origin="MYTPP", destination="TRGEM", vessel=9913547)

    assert shipment.calculate_fuel_costs(1500) == 2682050855.104

# Test to check if the returned ports are correct
# 1) amount check
# 2) keys check
# 3) values check
def test_get_ports():
    shipment = Shipment(
        id="78067E7F-D833-4312-A805-C1355F51F065", date=("2023, 1, 1"),
        cargo_weight=15649, distance_naut=5879.249, duration_hours=864.595, average_speed=6.8,
        origin="MYTPP", destination="TRGEM", vessel=9913547)

    assert len(shipment.get_ports()) == 2
    assert "origin" in shipment.get_ports()
    assert "destination" in shipment.get_ports()
    assert shipment.get_ports()["origin"].id == "MYTPP"
    assert shipment.get_ports()["destination"].id == "TRGEM"



# Test if the returned shipments contain the required shipment(s)
def test_get_shipments():
    vessel = Vessel(
    1034034, None, "GREAT WALL 17", "Tanzania", "Deck Cargo Ship", 2023, 1978, 2373, 84, 19)

    assert len(vessel.get_shipments()) > 0
