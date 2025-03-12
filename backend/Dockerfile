FROM python:3.13.1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY models.py config.py app.py search.py seed.py tasks.py .

COPY routes/ routes/

COPY utils/ utils/

EXPOSE 5000

CMD ["python", "app.py"]
