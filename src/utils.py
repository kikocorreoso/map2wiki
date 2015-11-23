import urllib.request
import json

import wikipedia as wp
from flask.ext.babel import gettext

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
    
def get_wiki_info(title, lang):
    """This function retrieves information from the Wikipedia API.
    
    :param title: A title of a possible wikipedia page
    :type title: str
    :returns: an object with information of the retrieved page
    :rtype: wikipedia.wikipedia.WikipediaPage object
    
    :Example:
    
    >>> result = get_wiki_info('Cervantes')
    >>> print(result.url)
    https://es.wikipedia.org/wiki/Miguel_de_Cervantes
    >>> print(result.title)
    Miguel de Cervantes
    >>> print(type(result))
    <class 'wikipedia.wikipedia.WikipediaPage'>
    >>> result = get_wiki_info('Cervantesssssssssssss')
    >>> print(type(result))
    <class 'str'>
    """
    wp.set_lang(lang)
    try:
        info = wp.page(title)
        return info
    except:
        msg = "<H2>We are sorry!</H2>\n"
        msg += "<p>We failed to offer you this service.</p>\n"
        msg += "<p>Return to the map and try ot again.</p>"
        return gettext(msg)

def parse_wiki_content(wikipage):
    """Function to parse the content of the Wikipedia article in a 
    simple way.
    
    Returns the article with some html tags.
    
    :param wikipage: The content of a wikipedia page as returned by
        wikipedia.wikipedia.WikipediaPage
    :type wikipage: str
    :returns: a string with the content with custom html formatting
    :rtype: str
    
    :Example:
    
    >>> page = get_wiki_info('Cervantes')
    >>> print(parse_wiki_content(page)[0:107])
    <H1><A href="https://es.wikipedia.org/wiki/Miguel_de_Cervantes" target="blank">Miguel de Cervantes</A></H1>
    >>> print(parse_wiki_content(page)[-93:-1])
    <P>Buscando a Miguel de Cervantes, monográfico en la Biblioteca Digital Memoriademadrid.</P>
    """
    result = """<H1><A href="{0}" target="blank">{1}</A></H1>\n"""
    result = result.format(wikipage.url, wikipage.title)
    for line in wikipage.content.split('\n'):
        if line.startswith('=') and line.endswith('='):
            h = int(line.count('=') / 2)
            line = line.replace("=", "") 
            result += "<H{0}>{1}</H{0}>\n".format(h, line)
        else:
            result += "    <P>{0}</P>\n".format(line)
    return result
