FROM python:3.9.0

RUN mkdir -p /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install our dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy the project code
COPY warehouse /app/warehouse
COPY run.py /app/

# expose the port
EXPOSE 7507

ENV FLASK_APP run.py
ENV FLASK_RUN_PORT 7507
ENV FLASK_ENV development

# define the default command to run when starting the container
CMD [ "flask", "run", "--host=0.0.0.0"]
