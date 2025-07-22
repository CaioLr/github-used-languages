from flask import Flask
from . import data_collector

app = Flask(__name__)

@app.route('/')
def get_used_languages():
    data = data_collector.fetch_data_from_api("CaioLr")
    return data

# @app.route('/<username>')
# def get_used_languages(username):
#     data = data_collector.fetch_data_from_api(username)
#     return data

if __name__ == '__main__':
    app.run(debug=True)