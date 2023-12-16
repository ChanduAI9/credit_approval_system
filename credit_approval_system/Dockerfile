FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copy only the requirements.txt,
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
