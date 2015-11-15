import urllib.request
import json

def get_address(lon, lat, service = "OSM"):
    """Get an address information from a geographical position using 
    OpenStreetMap Nominatim web service 
    (http://wiki.openstreetmap.org/wiki/Nominatim).
    
    It needs latitude and longitude as inputs and it returns a dict with
    information related with the address as the street name, the 
    country and the country code when possible or a dict with an `error`
    key indicating data couldn't be retrieved.
    
    :param lon: Longitude in degrees
    :param lat: Latitude in degrees
    :param service: Service to use for the reverse geocoding
    :type lon: int, float
    :type lat: int, float
    :type service: str
    :returns: a dict with data from a json response or with error info
    :rtype: dict
    
    :Example:
    
    >>> data = get_address(-1.81602098644987, 52.5487429714954)
    >>> print(data['display_name'])
    137, Pilkington Avenue, Castle Vale, Maney, Birmingham, West Midlands, England, B72 1LH, United Kingdom
    >>> print(data['address']['city'])
    Birmingham
    >>> print(data['lon'])
    -1.81627023283164
    >>> get_address(-40,40) # somewhere in the Atlantic Ocean
    {'NoDataError': 'No data on this location'}
    """
    if service == 'OSM':
        url = "http://nominatim.openstreetmap.org/reverse?"
        url += "format=json&lat={0}&lon={1}&zoom=18&addressdetails=1"
        url = url.format(lat, lon)
    else:
        # This is included only for testing purposes
        url = "http://example.com"
    try:
        resp = urllib.request.urlopen(url)
        data = json.loads(resp.read().decode('utf'))
        if 'error' in data.keys():
            return {'NoDataError': 'No data on this location'}
        else:
            return data
    except:
        return {'URLError': 'Cannot connect to URL'}

def isolate_name(street):
    """Enter the name of a street, road,..., and it tries to return a 
    sanitized string to be used in the wikipedia request
    
    :param street: a string with the address
    :type street: str
    :returns: a string with the address name sanitized
    :rtype: str
    
    :Example:
    
    >>> street = "Calle de Alfonso X"
    >>> print(isolate_name(street))
    alfonso x
    >>> avenue = "Avenida del rey Jaime III"
    >>> print(isolate_name(avenue))
    rey jaime iii
    >>> street = "Paseo de las delicias"
    >>> print(isolate_name(street))
    delicias
    """
    street = street.lower()
    pre = ["alameda", "avenida", "bulevar", "calle", "camino", 
           "carrera", "cuesta", "pasaje", "pasadizo", "paseo", "plaza", 
           "rambla", "ronda", "travesia", "via"]
    old = "áéíóúü"
    new = "aeiouu"
    for o, n in zip(old, new):
        street = street.replace(o, n)
    for prefij in pre:
        if prefij in street:
            street = street.replace(prefij + " ", "")
            if street.startswith("del "):
                street = street[4:]
            if street.startswith("de la "):
                street = street[6:]
            if street.startswith("de los "):
                street = street[7:]
            if street.startswith("de las "):
                street = street[7:]
            if street.startswith("de "):
                street = street[3:]
    return street
