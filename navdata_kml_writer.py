from navdata_types import *


def write_navdata_kml(output_path: str,
                      waypoints: list[Waypoint],
                      airports: list[Airport],
                      navaids: list[NavDataAidObject],
                      airways: list[Airway]):
    with open("kml_template.kml", "r", encoding="utf-8") as fin:
        template_str = fin.read()

        with open(output_path, "w", encoding="utf-8") as fout:
            fout.write(template_str.replace(
                "{WAYPOINTS}",
                "\n".join([item.get_placemark() for item in waypoints])
            ).replace(
                "{AIRPORTS}",
                "\n".join([item.get_placemark() for item in airports])
            ).replace(
                "{NAVAIDS}",
                "\n".join([item.get_placemark() for item in navaids])
            ).replace(
                "{AIRWAYS}",
                "\n".join([item.get_placemark() for item in airways])
            ))
