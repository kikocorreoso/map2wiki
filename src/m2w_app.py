from flask import Flask, render_template, request
from flask.ext.babel import Babel, gettext

from utils import (get_address, 
                   isolate_name, 
                   get_wiki_info,
                   parse_wiki_content)
from config import LANGUAGES

app = Flask(__name__)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return 'es' #return request.accept_languages.best_match(LANGUAGES.keys())

@app.route('/')
@app.route('/index')
def index():
    print(get_locale())
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
    lang = get_locale()
    print(lang)
    if lang not in ['en','es','fr']:
        lang = 'en'
    if request.method == 'POST':
        address = get_address(
            request.form['inputlon'],
            request.form['inputlat']
        )
        if address['address']['road']:
            title = isolate_name(address['address']['road'])
            article = get_wiki_info(title, lang)
            if isinstance(article, str):
                result = article
            else:
                result = parse_wiki_content(article)
            return render_template("wiki.html", 
                                   result = result,
                                   address = address)
        elif address['NoDataError']:
            return render_template("wiki.html",
                                   result = "<h2>:-(</h2>",
                                   address = address)
        elif address['UrlError']:
            return render_template("wiki.html",
                                   result = gettext("<h2>It seems we "
                                                    "cannot connect to "
                                                    "some service."
                                                    "</h2>"),
                                   address = address)
        else:
            return render_template("wiki.html",
                                   result = gettext("<h2>We don't know "
                                                    "what happened."
                                                    "</h2>"),
                                   address = address)
    
    
if __name__ == '__main__':
    app.run(debug = True)
