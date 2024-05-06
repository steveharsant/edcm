FROM python:3.12-alpine

LABEL author="steveharsant"

WORKDIR /app
COPY ./src .

RUN pip install -r requirements.txt
CMD ["python", "app.py"]
