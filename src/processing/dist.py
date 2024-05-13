import math

from geopy.geocoders import Nominatim


def calculate_distance(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371

    return c * r


def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    if calculate_distance(lat1, lon1, lat2, lon2) <= 0.5:
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


def get_code_location_dict():
    geolocation = Nominatim(user_agent="nlp")
    list_postal_codes = [str(48000 + x) for x in range(1, 16)]
    center_lat, center_lon = 43.263386002871265, -2.9371692887362872

    dict_cord_code = {}
    for code in list_postal_codes:
        location = geolocation.geocode(f"{code}, España")

        if not location:
            raise ValueError(f"The postal code {code} can not be found")

        dict_cord_code[code] = calculate_bearing(
            center_lat,
            center_lon,
            location.latitude,
            location.longitude,
        )

    return dict_cord_code
