FROM python:3.6

WORKDIR /app
COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt
CMD FLASK_APP=api.py flask run --host="::"