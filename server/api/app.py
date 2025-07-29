from flask import Flask, Response, request
from . import data_collector, db_connection, svg_creator
import os, json, requests, base64
from dotenv import load_dotenv # type: ignore
from datetime import datetime, timezone

load_dotenv()
app = Flask(__name__)

@app.route('/<username>')
def get_used_languages(username):
    config_arg_path = request.args.get('config')
    theme_arg = request.args.get('theme')
    db_connection.init_db()

    # =================== Getting the check information to avoid unnecessary requests ===================
    repositories_list = data_collector.get_repositories_list(username)
    db_last_update = db_connection.get_user_last_update(username)

    last_push = None
    for repo in repositories_list:
        repo_last_push =  datetime.fromisoformat(repo['pushed_at'].replace("Z", "+00:00"))
        if (not last_push or last_push < repo_last_push):
            last_push = repo_last_push

    # =================== Checking if DB is the updated one, if so, return the SVG from DB ===================
    if db_last_update:
        if last_push < db_last_update[0]:
            db_svg = db_connection.get_user_svg(username)
            db_svg = bytes(db_svg[1]).decode('utf-8') if theme_arg == 'dark' else bytes(db_svg[0]).decode('utf-8')
            return Response(db_svg, mimetype='image/svg+xml')

    # =================== Getting the config ===================
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

    # =================== Obtaining SVG and updating/inserting on DB ===================
    colors = (config['colors_light_theme'], config['colors_dark_theme'])
    data = data_collector.fetch_data(username, config, repositories_list)
    svg  = svg_creator.get_svg(data, config, colors)

    if db_last_update: # ========= Update =========
        db_connection.update_user_svg({
            'username':username,
            'last_update':datetime.now(timezone.utc),
            'svg_light': svg[0].encode('utf-8'),
            'svg_dark': svg[1].encode('utf-8')
        })
    if not db_last_update: # ========= Insert =========
        db_connection.insert_user_svg({
            'username':username,
            'last_update':datetime.now(timezone.utc),
            'svg_light': svg[0].encode('utf-8'),
            'svg_dark': svg[1].encode('utf-8')
        })
        db_connection.check_amount()

    return Response(svg, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)