from dotenv import load_dotenv
from os import getenv
import warnings
import logging
from zeep import Client
from zeep.plugins import HistoryPlugin
from lxml import etree
from pydantic import BaseModel

# Fast API
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Env vars
load_dotenv('.env')
port = getenv('PORT', default=3001)
log_level = getenv('LOGLEVEL', default='INFO')

# Config
logging.basicConfig(level=log_level.upper())
logger = logging.getLogger()
warnings.filterwarnings("ignore")
history = HistoryPlugin()

# Initialize soap client(s)
calculatorClient = Client(wsdl='http://www.dneonline.com/calculator.asmx?WSDL', plugins=[history])
# speedClient = Client('http://www.webservicex.net/ConvertSpeed.asmx?WSDL')

# Initialize Fast API app
app = FastAPI()

# Serve a page with some quick links
@app.get("/")
def home():
    html_content = """
    <html>
        <head>
            <title>SOAP Proxy</title>
        </head>
        <body>
            <main>
                <h1>SOAP Proxy</h1>
                <a href='/add?x=4&y=7'>Add example</a>
                <br />
                <a href='/subtract?x=13&y=4'>Subtract example</a>
                <br />
                <a href='/divide?x=12&y=3'>Divide example</a>
                <br />
                <a href='/multiply?x=4&y=7'>Multiply example</a>
            </main>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Type the fn signatures for OpenApi spec
class Response(BaseModel):
    operation: str
    result: int
    soap_request: str
    soap_response: str

# Main operations
@app.get("/add")
def add(x: int, y: int) -> Response:
    result = calculatorClient.service.Add(x, y)
    xml = get_xml()
    return { "operation": "add", "result": result, "soap_request": xml[0], "soap_response": xml[1] }

@app.get("/subtract")
def subtract(x: int, y: int) -> Response:
    result = calculatorClient.service.Subtract(x, y)
    xml = get_xml()
    return { "operation": "subtract", "result": result, "soap_request": xml[0], "soap_response": xml[1]  }

@app.get("/multiply")
def multiply(x: int, y: int) -> Response:
    result = calculatorClient.service.Multiply(x, y)
    xml = get_xml()
    return { "operation": "multiply", "result": result, "soap_request": xml[0], "soap_response": xml[1]  }

@app.get("/divide")
def divide(x: int, y: int) -> Response:
    result = calculatorClient.service.Divide(x, y)
    xml = get_xml()
    return { "operation": "divide", "result": result, "soap_request": xml[0], "soap_response": xml[1]  }

# Helpers
def get_xml():
    req_xml = etree.tostring(history.last_sent["envelope"], encoding="us-ascii", pretty_print=True)
    res_xml = etree.tostring(history.last_received["envelope"], encoding="us-ascii", pretty_print=True)
    return (req_xml, res_xml)

if __name__ == '__main__':
    logger.info(f"-- Starting server on port {port}")
    uvicorn.run("main:app", port=int(port), reload=True)
