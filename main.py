from dotenv import load_dotenv
from os import getenv
from flask import Flask, request, jsonify
import warnings
import logging
from zeep import Client

logging.basicConfig(level=logging.DEBUG)
warnings.filterwarnings("ignore")

# Env vars
load_dotenv('.env')
port = getenv('PORT', default=3001)
debug = getenv('DEBUG', default=False)

# Initialize soap client
soapClient = Client(wsdl='http://www.dneonline.com/calculator.asmx?WSDL')

# Initialize Flask app
app = Flask(__name__)

@app.route('/add',methods = ['GET'])
def add():
    x = request.args.get('x')
    y = request.args.get('y')
    print(x)
    print(y)
    if not x or not y:
        body = jsonify({ "error": "Missing argument(s)" })
        return body, 400
    else:
        result = soapClient.service.Add(x, y)
        return jsonify({ "result": result })

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port, debug=debug)

