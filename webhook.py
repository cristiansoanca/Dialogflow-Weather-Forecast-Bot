import requests

from flask import Flask
from flask import request
from flask import jsonify


# Flask app should start in global layout
app = Flask(__name__)


def makeResponse(dialogflow_data):
    result = dialogflow_data.get('queryResult')
    parameters = result.get('parameters')
    city = parameters.get('geo-city')
    date = parameters.get('date-time').split('T')[0]

    # Weather API
    r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=2cbe6a057de3aadd1d2353cf765a1895")
    json_object = r.json()
    weather = json_object['list']
    for i in range(len(weather)):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break

    speech = f"The forecast for {city} on {date} is {condition}"

    return {'fulfillmentText': speech}


@app.route('/webhook', methods=['POST'])
def webhook():
    dialogflow_data = request.get_json(silent=True)
    return jsonify(makeResponse(dialogflow_data))


@app.route("/", methods=['GET'])
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()


