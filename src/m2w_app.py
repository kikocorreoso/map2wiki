from flask import Flask, render_template, request

from utils import (get_address, 
                   isolate_name, 
                   get_wiki_info,
                   parse_wiki_content)

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    lon = -3.7035
    lat = 40.4171
    zoom = 4
    if request.args.get('lon'):
        lon = float(request.args.get('lon'))
    if request.args.get('lat'):
        lat = float(request.args.get('lat'))
    if request.args.get('zoom'):
        zoom = float(request.args.get('zoom'))
    return render_template('index.html', 
                           lon = lon, 
                           lat = lat, 
                           zoom = zoom)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/wiki', methods = ['POST'])
def wiki():
    if request.method == 'POST':
        address = get_address(
            request.form['inputlon'],
            request.form['inputlat']
        )
        if 'road' in address['address'].keys():
            title = isolate_name(address['address']['road'])
            article = get_wiki_info(title)
            if isinstance(article, str):
                result = article
            else:
                result = parse_wiki_content(article)
            return render_template("wiki.html", 
                                   result = result,
                                   address = address)
        elif 'pedestrian' in address['address'].keys():
            title = isolate_name(address['address']['pedestrian'])
            article = get_wiki_info(title)
            if isinstance(article, str):
                result = article
            else:
                result = parse_wiki_content(article)
            return render_template("wiki.html", 
                                   result = result,
                                   address = dict(address))
        elif address['NoDataError']:
            return render_template("wiki.html",
                                   result = "<h2>:-(</h2>",
                                   address = dict(address))
        elif address['UrlError']:
            return render_template("wiki.html",
                                   result = ("<h2>Parece que no "
                                             "podemos conectar a "
                                             "alguno de los servicios "
                                             "que usa la aplicación."
                                             "</h2>"),
                                   address = address)
        else:
            return render_template("wiki.html",
                                   result = ("<h2>No sabemos qué ha "
                                             "pasado. Lo sentimos en "
                                             "más profundo de nuestro "
                                             "frágil corazón</h2>"),
                                   address = address)
    
    
if __name__ == '__main__':
    app.run(debug = True, port = 5000)
