FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files
COPY DjangoAgentDashboard /app/
RUN ls /app
EXPOSE 8000

CMD ["gunicorn", "DjangoAgentDashboard.wsgi:application", "--bind", "0.0.0.0:8000"]
