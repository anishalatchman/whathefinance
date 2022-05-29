# Instance of this is our kind of basic application.
from flask import Flask
from flask import request
from flask_cors import CORS

import model

app = Flask(__name__)
#TODO: Unsafe -- but we're just playing here.
CORS(app)

# Specify what URL triggers the function
@app.route("/hello")
def hello_world():
    # Default content type is HTML, so browser will render this string as HTML.
    return "<p>Hello, World!</p>"

# simply handle the GET requests.
@app.route('/<browser>/<crappy_keywords>')
def handle_request(browser: str, crappy_keywords: str) -> dict:
    """Handle a GET request from Anisha's front-end -- take the input keyword
    and browser specification. Use model functions to compute them and output
    as JSON.

    Use model functions for the actual computation.

    Preconditions
    - browser in {'Firefox', 'Chrome'}
    - keywords consists of keyword strings separated by dashes. e.g.
    'my-key-words'.
    """
    # Format the keywords nicely.
    keywords = crappy_keywords.split('-')
    # Get the URLs
    article_links = model.find_articles(keywords, browser)
    # Summarize their articles!
    result = model.summarize_articles(article_links, browser)
    # Flask will convert a dictionary into JSON automagically! :D
    return result





