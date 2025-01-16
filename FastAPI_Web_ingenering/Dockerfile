FROM python:3.7

COPY . /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]