FROM python:3.9

COPY ./ccfdml /ccfdml
WORKDIR /ccfdml

RUN pip install -r /ccfdml/requirements.txt

EXPOSE 8891

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8891"]
