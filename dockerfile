FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

COPY /requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/
WORKDIR /code

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
