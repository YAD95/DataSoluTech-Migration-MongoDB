FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY code_migration.py .
COPY healthcare_dataset.csv .

CMD ["python", "code_migration.py"]