from flask import Flask, Response, request
from . import data_collector, svg_creator
import os, json, requests, base64
from dotenv import load_dotenv
from ..db import scripts_db
from datetime import datetime, timezone

load_dotenv()
app = Flask(__name__)

@app.route('/<username>')
def get_used_languages(username):
    config_arg_path = request.args.get('config')
    scripts_db.init_db()

    repositories_list = data_collector.get_repositories_list(username)
    last_push = None

    for repo in repositories_list:
        repo_last_push =  datetime.fromisoformat(repo['pushed_at'].replace("Z", "+00:00")).timestamp()
        if (not last_push or last_push < repo_last_push):
            last_push = repo_last_push

    db_last_update = scripts_db.get_user_last_update(username)

    if db_last_update:
        if last_push < db_last_update[0]:
            db_svg = scripts_db.get_user_svg(username)
            db_svg = db_svg[0].decode('utf-8')
            return Response(db_svg, mimetype='image/svg+xml')

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

    data = data_collector.fetch_data_from_api(username, config, repositories_list)
    svg  = svg_creator.create_svg(data,config)

    if db_last_update:
        scripts_db.update_user_svg({
            'username':username,
            'last_update':datetime.now(timezone.utc).timestamp(),
            'svg': svg.encode('utf-8')
        })
    if not db_last_update:
        scripts_db.insert_user_svg({
            'username':username,
            'last_update':datetime.now(timezone.utc).timestamp(),
            'svg': svg.encode('utf-8')
        })
        scripts_db.check_amount()

    return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)