FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip==24.2
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
