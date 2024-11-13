# SOAP - REST Proxy

This flask server is an example of how to proxy REST api calls to a SOAP service. This server will expose REST endpoints which can be called from watsonx orchestrate, and then corresponding SOAP services will be called, and the response sent back to wxo.

## Dev setup
- Python
- 1. Create venv
- 2. Install dependencies
- 3. Run main.py