"""
FROM python:3.11-slim
WORKDIR /app


# copy files
COPY . /app


# create data dir for sqlite persistence
RUN mkdir -p /app/data


# Install optional dependencies (rich + pytest)
RUN pip install --no-cache-dir -r requirements.txt


ENV PYTHONUNBUFFERED=1


CMD ["python", "app.py"]
"""
