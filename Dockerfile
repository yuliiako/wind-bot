FROM python:3.7-slim

WORKDIR /home/wind_bot

COPY . .

RUN pip install -r requirements.txt

RUN python create_db.py

CMD python main.py