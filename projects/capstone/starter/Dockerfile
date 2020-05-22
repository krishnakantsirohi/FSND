FROM python:slim
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install -r requirements.txt


ENTRYPOINT ["./gunicorn.sh"]