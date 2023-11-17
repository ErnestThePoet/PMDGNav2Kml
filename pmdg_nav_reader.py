from typing import Iterable, Callable
import geopy.distance
from navdata_types import *


def read_pmdg_navdata_lines(file_path: str) -> Iterable[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return filter(lambda item: not item.startswith(";"), f.readlines())


def read_pmdg_aid_list(file_path: str,
                       filter_pred: Callable[[NavDataAidObject], bool] | None = None) -> list[NavDataAidObject]:
    result: list[NavDataAidObject] = []
    for i in read_pmdg_navdata_lines(file_path):
        navaid_name = i[:24].strip()
        navaid_code = i[24:29].strip()
        navaid_type = i[29:33].strip()
        navaid_lat = i[33:43].strip()
        navaid_lon = i[43:54].strip()
        navaid_freq = i[54:].strip()[:-1]
        navaid_class = i[54:].strip()[-1:]

        current: NavDataAidObject | None = None

        if navaid_type == "VORD":
            current = VorDme(navaid_code,
                             navaid_lat,
                             navaid_lon,
                             navaid_name,
                             navaid_freq,
                             navaid_class)
        elif navaid_type == "VOR":
            current = Vor(navaid_code,
                          navaid_lat,
                          navaid_lon,
                          navaid_name,
                          navaid_freq,
                          navaid_class)
        elif navaid_type == "DME":
            current = Dme(navaid_code,
                          navaid_lat,
                          navaid_lon,
                          navaid_name,
                          navaid_freq,
                          navaid_class)
        elif navaid_type == "NDB":
            current = Ndb(navaid_code,
                          navaid_lat,
                          navaid_lon,
                          navaid_name,
                          navaid_freq)

        if current is not None and (filter_pred is None or filter_pred(current)):
            result.append(current)

    return result


def read_pmdg_airport_list(dat_file_path: str,
                           navapt_file_path: str,
                           filter_pred: Callable[[Airport], bool] | None = None) -> list[Airport]:
    result: list[Airport] = []

    airports_map: dict[str, Airport] = {}

    for i in read_pmdg_navdata_lines(dat_file_path):
        airport_icao = i[:4].strip()
        airport_lat = i[4:14].strip()
        airport_lon = i[14:].strip()

        airports_map[airport_icao] = Airport(airport_icao, airport_lat, airport_lon, "", [])

    for i in read_pmdg_navdata_lines(navapt_file_path):
        airport_name = i[:24].strip()
        airport_icao = i[24:28].strip()
        airport_runway_number = i[28:31].strip()
        airport_runway_length_m = round(int(i[31:36].strip()) * 0.3048)
        airport_runway_elev_ft = int(i[69:].strip())
        airport_runway_ils_freq = i[60:66].strip()
        airport_runway_ils_crs = i[66:69].strip()

        airports_map[airport_icao].name = airport_name

        if airport_runway_ils_freq == "000.00":
            airports_map[airport_icao].runways.append((
                airport_runway_number,
                airport_runway_length_m,
                airport_runway_elev_ft
            ))
        else:
            airports_map[airport_icao].runways.append((
                airport_runway_number,
                airport_runway_length_m,
                airport_runway_elev_ft,
                airport_runway_ils_freq,
                airport_runway_ils_crs
            ))

    for i in airports_map:
        if filter_pred is None or filter_pred(airports_map[i]):
            result.append(airports_map[i])

    return result


def read_pmdg_waypoint_list(file_path: str,
                            filter_pred: Callable[[Waypoint], bool] | None = None) -> list[Waypoint]:
    result: list[Waypoint] = []

    for i in read_pmdg_navdata_lines(file_path):
        waypoint_code = i[:5].strip()
        waypoint_lat = i[29:39].strip()
        waypoint_lon = i[39:].strip()

        current = Waypoint(waypoint_code, waypoint_lat, waypoint_lon)

        if filter_pred is None or filter_pred(current):
            result.append(current)

    return result


def read_pmdg_airway_list(file_path: str,
                          filter_pred: Callable[[Airway], bool] | None = None) -> list[Airway]:
    result: list[Airway] = []

    current_airway_data = ["", []]

    for i in read_pmdg_navdata_lines(file_path):
        splitted = i.strip().split(" ")
        if current_airway_data[0] == "" or \
                (splitted[0] == current_airway_data[0] and (
                        len(current_airway_data[1]) == 0 or
                        geopy.distance.distance(
                            (float(current_airway_data[1][len(current_airway_data[1]) - 1][2]),
                             float(current_airway_data[1][len(current_airway_data[1]) - 1][3])),
                            (float(splitted[3]), float(splitted[4]))).nautical <= 1000)):
            current_airway_data[0] = splitted[0]
            current_airway_data[1].append((
                int(splitted[1]),
                splitted[2],
                splitted[3],
                splitted[4],
            ))
        else:
            current_airway_data[1].sort(key=lambda item: item[0])
            current = Airway(current_airway_data[0],
                             [item[1] for item in current_airway_data[1]],
                             [(item[2], item[3]) for item in current_airway_data[1]])

            if filter_pred is None or filter_pred(current):
                result.append(current)

            current_airway_data = [splitted[0], [(
                int(splitted[1]),
                splitted[2],
                splitted[3],
                splitted[4],
            )]]

    return result
