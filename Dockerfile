FROM python:3.12.0-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4000
CMD ["uvicorn", "main:app", "--port","4000", '--reload']