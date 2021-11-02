FROM python:3.9-buster

ADD main.py .
ADD config.py .

RUN pip install pyTelegramBotAPI 

CMD [ "python", "./main.py" ]