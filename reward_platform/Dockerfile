FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements-test.txt ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-test.txt

COPY . .

# Make entrypoint script executable and set proper permissions
RUN chmod +x /app/entrypoint.sh && \
    chown -R root:root /app && \
    chmod -R 755 /app

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
