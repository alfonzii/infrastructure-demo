FROM python:3.10-alpine
ADD . /code
WORKDIR /code
RUN python3 -m pip install -r requirements.txt
CMD ["python", "web-app.py"]
