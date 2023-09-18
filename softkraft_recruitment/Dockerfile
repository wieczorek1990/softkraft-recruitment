FROM python:3.11-alpine

# Virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Dependencies installation
WORKDIR /root/
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

# Application
WORKDIR /opt/app/
COPY . .

# User & group
RUN addgroup -S non-root && adduser -S non-root -G non-root
USER non-root

EXPOSE 8000
CMD ["sh", "run.sh"]
