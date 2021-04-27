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

 
def extract_ticket_data(dialogflow_data):
    result = dialogflow_data.get('queryResult')
    parameters = result.get('parameters')
    ticket_number = parameters.get('incident')

    # Get ticket data
    url = "https://auchan.easyvista.com/api/v1/50004/internalqueries"
    querystring = {
            "queryguid": "51A131C1-5C8D-4CD0-895A-A353F02BB6B4",
            "filterguid": "8A0535F5-03E8-4175-AEEC-40384D062074",
            "viewguid": "82970C26-B9DF-4C00-B79C-3BF1AF041AB0",
            "custom_filter": f"(( SD_REQUEST.RFC_NUMBER = '{ticket_number}'))",
            "max_rows": "1111"
        }
    payload = ""
    headers = {
        'Authorization': "Basic bW9td2ViOmF1Y2hhbg==",
        'content-type': "application/json"
    }

    try:
        response = requests.request(
            "GET",
            url,
            data=payload,
            headers=headers,
            params=querystring
        )
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    r = response.json()['records']

    return {'fulfillmentText': r}


@app.route('/webhook', methods=['POST'])
def webhook():
    dialogflow_data = request.get_json(silent=True)
    if "weather" in dialogflow_data.get("queryText") or \
        "forecast" in dialogflow_data.get("queryText"):
            return jsonify(makeResponse(dialogflow_data))
    else:
            return jsonify(extract_ticket_data(dialogflow_data))


@app.route('/', methods=['GET'])
def hello():
    return 'hello world!'
