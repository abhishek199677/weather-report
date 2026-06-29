FROM python:3.11-slim
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY client/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY client/api_client.py client/app.py ./
USER app
EXPOSE 8501
ENV PYTHONUNBUFFERED=1
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
