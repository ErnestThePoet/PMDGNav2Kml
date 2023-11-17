import abc
from abc import ABC

LF = "\n"


class NavDataObject:
    def __init__(self, code: str):
        self.code = code

    @abc.abstractmethod
    def get_placemark(self) -> str:
        pass


class NavDataPointObject(NavDataObject, ABC):
    def __init__(self, code: str, lat_str: str, lon_str: str):
        super(NavDataPointObject, self).__init__(code)
        self.lat_str = lat_str
        self.lon_str = lon_str
        self.lat = float(lat_str)
        self.lon = float(lon_str)


class NavDataAidObject(NavDataPointObject, ABC):
    def __init__(self, code: str, lat_str: str, lon_str: str, name: str, freq: str):
        super(NavDataAidObject, self).__init__(code, lat_str, lon_str)
        self.name = name
        self.freq = freq


class Waypoint(NavDataPointObject):
    def __init__(self, code: str, lat_str: str, lon_str: str):
        super(Waypoint, self).__init__(code, lat_str, lon_str)

    def get_placemark(self):
        return get_point_placemark(self, "Waypoint", "#msn_triangle")


class Airport(NavDataPointObject):
    def __init__(self, code: str, lat_str: str, lon_str: str,
                 name: str,
                 runways: list[tuple[str, int, int] | tuple[str, int, int, str, str]]):
        super(Airport, self).__init__(code, lat_str, lon_str)
        self.name = name
        self.runways = runways

    def get_placemark(self):
        runway_info = "\n".join(map(
            lambda item:
            f"RWY{item[0]} {item[1]}m{f' ILS {item[3]}/{item[4]}' if len(item) == 5 else ''} Elev {item[2]}ft",
            self.runways))
        return get_point_placemark(self, "Airport", "#msn_placemark_circle", [self.name, runway_info])


class VorDme(NavDataAidObject):
    def __init__(self, code: str, lat_str: str, lon_str: str,
                 name: str, freq: str, class_type: str):
        super(VorDme, self).__init__(code, lat_str, lon_str, name, freq)
        self.class_type = class_type

    def get_placemark(self):
        return get_point_placemark(self, "VOR/DME", "#msn_target",
                                   [self.name, self.freq, f"Class {self.class_type}"])


class Vor(NavDataAidObject):
    def __init__(self, code: str, lat_str: str, lon_str: str,
                 name: str, freq: str, class_type: str):
        super(Vor, self).__init__(code, lat_str, lon_str, name, freq)
        self.class_type = class_type

    def get_placemark(self):
        return get_point_placemark(self, "VOR", "#msn_square",
                                   [self.name, self.freq, f"Class {self.class_type}"])


class Dme(NavDataAidObject):
    def __init__(self, code: str, lat_str: str, lon_str: str,
                 name: str, freq: str, class_type: str):
        super(Dme, self).__init__(code, lat_str, lon_str, name, freq)
        self.class_type = class_type

    def get_placemark(self):
        return get_point_placemark(self, "DME", "#msn_polygon",
                                   [self.name, self.freq, f"Class {self.class_type}"])


class Ndb(NavDataAidObject):
    def __init__(self, code: str, lat_str: str, lon_str: str,
                 name: str, freq: str):
        super(Ndb, self).__init__(code, lat_str, lon_str, name, freq)

    def get_placemark(self):
        return get_point_placemark(self, "NDB", "#msn_donut", [self.name, self.freq])


class Airway(NavDataObject):
    def __init__(self, code: str,
                 waypoint_codes: list[str],
                 waypoint_coords_str: list[tuple[str, str]]):
        super(Airway, self).__init__(code)
        self.waypoint_codes = waypoint_codes
        self.waypoint_coords_str = waypoint_coords_str
        self.waypoint_coords = list(map(
            lambda item: [float(item[0]), float(item[1])], waypoint_coords_str))

    def get_placemark(self):
        return get_airway_placemark(self)


def get_point_placemark(obj: NavDataPointObject,
                        obj_type: str,
                        style_url: str,
                        extra_desc_lines: list[str] = None):
    if extra_desc_lines is None:
        extra_desc_lines = []

    return f"""
        <Placemark>
            <name>{obj.code}</name>
            <visibility>0</visibility>
            <description>{LF.join([f"{obj.code} {obj_type}"] + extra_desc_lines)}</description>
            <LookAt>
                <longitude>{obj.lon_str}</longitude>
                <latitude>{obj.lat_str}</latitude>
                <altitude>0</altitude>
                <heading>0</heading>
                <tilt>0</tilt>
                <range>60000</range>
                <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
            </LookAt>
            <styleUrl>{style_url}</styleUrl>
            <Point>
                <gx:drawOrder>1</gx:drawOrder>
                <coordinates>{obj.lon_str},{obj.lat_str},0</coordinates>
            </Point>
        </Placemark>
    """


def get_airway_placemark(airway: Airway):
    return f"""
        <Placemark>
            <name>{airway.code}</name>
            <visibility>0</visibility>
            <description>{airway.code} Airway
            {LF.join(airway.waypoint_codes)}
            </description>
            <styleUrl>#inline</styleUrl>
            <LineString>
                <tessellate>1</tessellate>
                <coordinates>
                {" ".join(map(lambda item: f"{item[1]},{item[0]},0", airway.waypoint_coords))}
                </coordinates>
            </LineString>
        </Placemark>
    """
