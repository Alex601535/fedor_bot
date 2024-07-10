FROM python:3.9-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY fedor_bot.py .

CMD ["python", "fedor_bot.py"]
