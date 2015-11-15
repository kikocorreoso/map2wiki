import urllib.request, json

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
    :param service: Service to use for the reverse geocoding.
    :type arg1: int, float
    :type arg2: int, float
    :returns: data from a json response
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
