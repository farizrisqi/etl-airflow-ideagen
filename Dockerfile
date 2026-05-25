FROM apache/airflow:2.7.1-python3.10

USER root
# Install dependencies sistem yang dibutuhkan Playwright
RUN apt-get update && apt-get install -y \
    libgbm1 \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libasound2 \
    gnumeric \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER airflow
# Install library python dan browser playwright
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
ENTRYPOINT ["/entrypoint.sh"]