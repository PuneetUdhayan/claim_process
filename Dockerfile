FROM python

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]