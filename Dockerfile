FROM python:3.10

# Install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

# Install utility for getting docker secrets
RUN pip install --no-cache-dir get-docker-secret

# Copy app
COPY . .

CMD [ "python", "bot.py" ]