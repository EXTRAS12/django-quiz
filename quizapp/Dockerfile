FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /crm

COPY ./requirements.txt /crm/requirements.txt
RUN pip install -r /crm/requirements.txt

COPY . /crm

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
