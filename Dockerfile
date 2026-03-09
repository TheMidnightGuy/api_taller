FROM python:3.12.0-slim
WORKDIR /app
RUN mkdir -p /app/log
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port","4000"]