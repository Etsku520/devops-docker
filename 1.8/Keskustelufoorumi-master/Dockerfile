FROM ubuntu:16.04

WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y python3.5
RUN apt-get install -y nginx git python-setuptools python-dev
RUN easy_install pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
