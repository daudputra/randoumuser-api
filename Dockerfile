FROM python:3.12.1

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 3030

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
