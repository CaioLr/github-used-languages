from flask import Flask, Response
from . import data_collector, svg_creator
import os
import json

app = Flask(__name__)

@app.route('/')
def get_default_used_languages():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'default_config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)

    data = data_collector.fetch_data_from_api("CaioLr",  config)
    return data

@app.route('/<username>')
def get_used_languages(username):

    config_path = os.path.join(os.path.dirname(__file__), '..', 'default_config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)

    data = data_collector.fetch_data_from_api(username, config)
    svg  = svg_creator.create_svg(data,config)

    return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)