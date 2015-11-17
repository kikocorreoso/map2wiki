# map2wiki

Simple flask app to obtain wikipedia information from an address. You can see a demo [here](http://map2wiki.runbear.webfactional.com/).

## How to use the demo

![mapa](https://raw.githubusercontent.com/kikocorreoso/map2wiki/master/img/Home.png)

Center the map on a street, avenue, square,..., and click on **Search address history**. 
Alternatively, you can click on **Get my position** and let the browser geolocalise your position.

Example for *[Calle de Juan Bravo, Madrid,
Spain](http://map2wiki.runbear.webfactional.com/index?lon=-3.68482&lat=40.43294&zoom=18)*.

![Mapa Juan Bravo](https://raw.githubusercontent.com/kikocorreoso/map2wiki/master/img/JuanBravoMap.png)

If you click on the left button (**Search address history**), you should go to a page like this one:

![Resultado Juan Bravo](https://raw.githubusercontent.com/kikocorreoso/map2wiki/master/img/JuanBravoWiki.png)

There you have the result of the request to the [OpenStreetMap nominatim API](http://wiki.openstreetmap.org/wiki/Nominatim) in json format, 
and the request obtained from the wikipedia API.

## Motivation

The other day I was waiting for a friend and during that time I thought -'I have no idea who is Juan Bravo'-. 

Why not open your browser and go directly to the Wikipedia? Because this way I don't learn about
[Nominatim](http://wiki.openstreetmap.org/wiki/Nominatim), [Wikipedia
API](https://www.mediawiki.org/wiki/API:Main_page), [Flask](http://flask.pocoo.org/),
[Openlayers](http://openlayers.org/), [Brython](http://brython.info/), CSS hell,...

![css hell](https://raw.githubusercontent.com/kikocorreoso/map2wiki/master/img/CSSHell.gif)

## TODO

* Right now, it works only for addresses and results in spanish. If you want to see other languages working, 
please, [open an issue](https://github.com/kikocorreoso/map2wiki/issues) with the language you want to 
include and a complete list of possible *types* of addresses. For example, in english it could be 
*street*, *avenue*, *square*,... In spanish I am using the following list: *alameda, avenida, bulevar, calle, camino, 
carrera, cuesta, pasaje, pasadizo, paseo, plaza, rambla, ronda, travesia, via*.
* Fix some stuff to make it more Flask way (`url_for`, static folder,...).
* Include a minified version of brython in the distribution.
* Add tests for the Flask part.
* ...

## Issues

Of course, it has bugs, if you find one, please, send me as much info as possible to try to reproduce 
the error and fix it.

## How to run locally

Instructions to run it on *nix using a virtualenv and Python >= 3.3:

`git clone https://github.com/kikocorreoso/map2wiki.git`

`cd map2wiki/`

`python -m venv env # I assume you are using Python 3, if not, you should!!`

`. env/bin/activate`

`pip install -r requirements.txt`

`cd src/`

`python m2w_app.py`

Open your browser and go to http://localhost:5000

If you want to deploy the app somewhere edit the [last line on m2w_app.py](https://github.com/kikocorreoso/map2wiki/blob/master/src/m2w_app.py#L64) in order to not 
use the `debug` mode:

Change `    app.run(debug = True)` to `    app.run()`

## Dependencies

* [Flask](http://flask.pocoo.org/)
* [Wikipedia python package](https://pypi.python.org/pypi/wikipedia/1.4.0)

Thanks to the developers of the packages listed above!!
