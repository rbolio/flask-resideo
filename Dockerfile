FROM python:alpine3.10

RUN apk add --update gcc

RUN mkdir /app
COPY dist/*.whl /app
WORKDIR /app

# ARGS
ARG user_name
ARG user_pwd
ARG database_db
ARG db_host
ARG db_port

# ENV
ENV user_name=${user_name}
ENV user_pwd=${user_pwd}
ENV database_db=${database_db}
ENV db_host=${db_host}
ENV db_port=${db_port}

# Build
RUN pip install *.whl
EXPOSE 5000

# Run
CMD [ "flaskr" ]
