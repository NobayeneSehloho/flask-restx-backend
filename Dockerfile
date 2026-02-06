FROM python:3.12-alpine

WORKDIR /app

# Install build dependencies and curl
RUN apk add --no-cache gcc musl-dev g++ postgresql-dev curl

# Upgrade pip to latest
RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size (keep curl)
RUN apk del gcc musl-dev g++

COPY app ./app

ENV FLASK_APP=app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["flask", "run", "--host=0.0.0.0"]