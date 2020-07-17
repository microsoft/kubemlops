from flask import Flask, request
import random


application = Flask(__name__)


#  Randomly route to either 1st or 2nd child
@application.route("/route", methods=['GET', 'POST'])
def route():
    if (request.method == 'GET'):
        return "Healthy"
    else:
        payload = request.get_json()
        print(f'Route message: {payload}')
        child = random.randint(0, 1)

        return '{"data":{"ndarray":[' + str(child) + ']}}'


#  Prediction is emulated by incrementing the input payload
#  e.g {"data":"0"} -> {"data":"1"}
@application.route("/predict", methods=['GET', 'POST'])
def predict() -> str:
    if (request.method == 'GET'):
        return "Healthy"
    else:
        payload = request.get_json()
        print(f'Input message: {payload}')

        data = int(payload['data'])
        data = data + 1

        return '{"data":"' + str(data) + '"}'


#  Aggregate the output of two children by concatanating
#  e.g. {"data":"101"},{"data":"101"} ->  {"data":"101101"}
@application.route("/aggregate", methods=['GET', 'POST'])
def aggregate():
    if (request.method == 'GET'):
        return "Healthy"
    else:
        payload = request.get_json()
        print(f'Combine message: {payload}')

        combined_data = payload[0]['data'] + payload[1]['data']
        return '{"data":"' + str(combined_data) + '"}'


#  Tranform the input data by adding 100 to the payload
#  e.g. {"data":"0"} -> {"data":"100"}
@application.route("/transform-input", methods=['GET', 'POST'])
def transform_input():
    if (request.method == 'GET'):
        return "Healthy"
    else:
        payload = request.get_json()
        print(f'Transform input message: {payload}')

        data = int(payload['data'])
        data = data + 100

        return '{"data":"' + str(data) + '"}'


#  Put the output data into the "prediction" json
#  e.g. {"data":"102"} -> {"prediction_result":"102"}
@application.route("/transform-output", methods=['GET', 'POST'])
def transform_output():
    if (request.method == 'GET'):
        return "Healthy"
    else:
        payload = request.get_json()
        print(f'Transform output message: {payload}')

        return '{"prediction_result":"' + payload['data'] + '"}'


if __name__ == "__main__":
    application.run(host='0.0.0.0')
