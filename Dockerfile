FROM python:3.11

# Install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

# Install utility for getting docker secrets
RUN pip install --no-cache-dir get-docker-secret

# Copy app
COPY . .

CMD [ "python", "-u", "bot.py" ]