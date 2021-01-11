FROM python:3.8
ENV PYTHONUNBUFFERED=1
ADD . hw6/
WORKDIR hw6
RUN pip install -r requirements.txt

ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:9000"]
