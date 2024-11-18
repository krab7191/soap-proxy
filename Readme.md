# SOAP - REST Proxy

This flask server is an example of how to proxy REST api calls to a SOAP service. This server will expose REST endpoints which can be called from watsonx orchestrate, and then corresponding SOAP services will be called, and the response sent back to wxo.

## Dev setup
- Python
- 1. Create venv
- 2. Install dependencies
- 3. Run main.py

## Docker
- `docker build -t soap-proxy .`
- `docker image ls` to check images
- `docker run -p 80:3001 --expose 80 soap-proxy:latest` to test (add -d flag to detach shell)
  - Navigate to `http://localhost/add?x=7&y=4` as an example for /add endpoint.
- `docker ps -a` to list all containers


## Live 
- URL: https://soap-proxy.15tn84ngy7k3.us-east.codeengine.appdomain.cloud/
- 