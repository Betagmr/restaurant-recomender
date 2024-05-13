import math
import re

from geopy.geocoders import Nominatim


def add_direction_location(df_raw):
    new_df = df_raw.copy()
    new_df["direction"] = None
    dict_locations = _get_code_location_dict()

    for index, row in new_df.iterrows():
        direction = row["street"]
        if not isinstance(direction, str):
            continue

        is_zip_code = re.search(r"\b\d{5}\b", direction)
        if not is_zip_code:
            continue

        zip_code = is_zip_code.group(0)
        if zip_code not in dict_locations:
            continue

        new_df.loc[index, "direction"] = dict_locations[zip_code]

    return new_df


def _calculate_distance(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371

    return c * r


def _calculate_bearing(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    if _calculate_distance(lat1, lon1, lat2, lon2) <= 0.5:
        return "Centro"

    d_lon = lon2 - lon1
    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = math.atan2(y, x)

    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    directions = ["Norte", "Este", "Sur", "Oeste"]
    index = round(bearing / (360.0 / len(directions)))

    return directions[index % len(directions)]


def _get_code_location_dict():
    geolocation = Nominatim(user_agent="nlp")
    list_zip_codes = [str(48000 + x) for x in range(1, 16)]
    center_lat, center_lon = 43.263386002871265, -2.9371692887362872

    dict_cord_code = {}
    for code in list_zip_codes:
        location = geolocation.geocode(f"{code}, España")

        if not location:
            raise ValueError(f"The postal code {code} can not be found")

        dict_cord_code[code] = _calculate_bearing(
            center_lat,
            center_lon,
            location.latitude,
            location.longitude,
        )

    return dict_cord_code
