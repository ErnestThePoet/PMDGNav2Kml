import re

########## SETTINGS SECTION START ##########
# Set the range of lat and lon within which
# the waypoints and navaids are to be converted.
# Northern and Eastern are positive values.
LAT_MAX = 55.0
LAT_MIN = 30.0  # 17
LON_MAX = 135.0
LON_MIN = 100.0  # 73

# Placemark icons in Google Earth
STYLE_URLS = {
    "WPT": "#msn_triangle",
    "VOR": "#msn_open-diamond",
    "VORD": "#msn_square",
    "DME": "#msn_polygon",
    "NDB": "#m_ylw-pushpin"
}

# PMDG FIX and AID navdata file path
PMDG_AID_PATH = "wpNavAID.txt"
PMDG_FIX_PATH = "wpNavFIX.txt"

# Output kml path
OUTPUT_PATH = "output.kml"
########## SETTINGS SECTION END ##########

with open("placemark_template.txt", "r", encoding="utf-8") as f:
    template_str = f.read()

output_str = ""


def read_pmdg_aid_list(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        aid_lines = f.readlines()

    for i in aid_lines:
        if i.startswith(";"):
            continue
        lat = float(i[33:43].replace(" ", ""))
        lon = float(i[43:57].replace(" ", ""))
        if "ILS" not in i[29:33] \
                and LAT_MIN < lat < LAT_MAX \
                and LON_MIN < lon < LON_MAX:
            global output_str
            output_str += template_str.format(
                f"{i[24:29].replace(' ', '')}({i[0:24].replace(' ', '')})",
                lat,
                lon,
                STYLE_URLS[i[29:33].replace(" ", "")])


def read_pmdg_wpt_list(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        wpt_lines = f.readlines()

    for i in wpt_lines:
        if i.startswith(";"):
            continue
        if re.match("[0-9]{2}[NEWS][0-9]{2}", i[0:24]) is None \
                and re.match("[0-9]{4}[NEWS]", i[0:24]) is None:
            lat = float(i[29:39].replace(" ", ""))
            lon = float(i[39:50].replace(" ", ""))
            if LAT_MIN < lat < LAT_MAX \
                    and LON_MIN < lon < LON_MAX:
                global output_str
                output_str += template_str.format(
                    i[0:24].replace(' ', ''),
                    lat,
                    lon,
                    STYLE_URLS["WPT"])


read_pmdg_aid_list(PMDG_AID_PATH)
read_pmdg_wpt_list(PMDG_FIX_PATH)

with open("kml_template.txt", "r", encoding="utf-8") as f:
    output_str = f.read().format(output_str)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(output_str)
