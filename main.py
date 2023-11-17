import re
from navdata_types import *
from pmdg_nav_reader import *
from navdata_kml_writer import write_navdata_kml

CHINA_LAT_MIN = 17.0
CHINA_LAT_MAX = 55.0
CHINA_LON_MIN = 73.0
CHINA_LON_MAX = 145.0


def filter_latlon_waypoints(obj: Waypoint) -> bool:
    return re.match("[0-9]{2}[NEWS][0-9]{2}", obj.code) is None \
           and re.match("[0-9]{4}[NEWS]", obj.code) is None


def filter_latlon_waypoints_in_china(obj: Waypoint) -> bool:
    return re.match("[0-9]{2}[NEWS][0-9]{2}", obj.code) is None and \
           re.match("[0-9]{4}[NEWS]", obj.code) is None and \
           filter_point_in_china(obj)


def filter_point_in_china(obj: NavDataAidObject | Airport | Waypoint) -> bool:
    return CHINA_LAT_MIN <= obj.lat <= CHINA_LAT_MAX and \
           CHINA_LON_MIN <= obj.lon <= CHINA_LON_MAX


def filter_airway_in_china(obj: Airway) -> bool:
    return any([CHINA_LAT_MIN <= item[0] <= CHINA_LAT_MAX and \
                CHINA_LON_MIN <= item[1] <= CHINA_LON_MAX for item in obj.waypoint_coords])


waypoints = read_pmdg_waypoint_list("./NavData/wpNavFIX.txt", filter_latlon_waypoints_in_china)
airports = read_pmdg_airport_list("./NavData/airports.dat", "./NavData/wpNavAPT.txt", filter_point_in_china)
navaids = read_pmdg_aid_list("./NavData/wpNavAID.txt", filter_point_in_china)
airways = read_pmdg_airway_list("./NavData/wpNavRTE.txt", filter_airway_in_china)

write_navdata_kml("./out/china.kml",
                  waypoints,
                  airports,
                  navaids,
                  airways)
