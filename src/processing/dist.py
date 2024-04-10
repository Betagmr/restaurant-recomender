import math

def calculate_distance(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371

    return c * r


def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    if calculate_distance(lat1, lon1, lat2, lon2) <= 0.5:
        return "Centro"
    
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    bearing = math.atan2(y, x)

    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    directions = ["Norte", "Este", "Sur", "Oeste"]
    index = round(bearing / (360. / len(directions)))
    return directions[index % len(directions)]