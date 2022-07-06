FROM python:3.8-slim

COPY ./app /app
COPY ./requirements.txt /requirements.txt

EXPOSE 8000:8000

RUN python3 -m pip install -r requirements.txt

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]