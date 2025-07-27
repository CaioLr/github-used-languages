from flask import Flask, Response, request
from . import data_collector, svg_creator
import os, json, requests, base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def get_default_used_languages():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'default_config.json')
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    data = data_collector.fetch_data_from_api("CaioLr",  config)
    return data

@app.route('/<username>')
def get_used_languages(username):
    config_arg_path = request.args.get('config')
    
    if config_arg_path:
        headers = {
            "Authorization": f"Bearer {os.getenv('TOKEN')}",
            "Accept": "application/vnd.github+json"
        }

        try:
            response = requests.get(f'https://api.github.com/repos/{username}/{username}/contents/{config_arg_path}',headers=headers).json()
            config = json.loads(base64.b64decode(response['content']).decode('utf-8'))
        except:
            config_arg_path = None
        


    if not config_arg_path:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'default_config.json')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

    data = data_collector.fetch_data_from_api(username, config)
    svg  = svg_creator.create_svg(data,config)

    return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)