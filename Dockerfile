FROM python:3.10-slim-bullseye

ARG HNSWLIB_NO_NATIVE=1  
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

RUN mkdir /.cache
RUN ["chmod", "777","-R", "/.cache"]

WORKDIR /app
COPY . /app
RUN chmod -R 777 /app/

RUN pip3 install -r requirements.txt
EXPOSE 3001

ENTRYPOINT ["python3"]
CMD ["main.py"]
