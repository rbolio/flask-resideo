FROM python:alpine3.7
COPY dist/*.whl /app
WORKDIR /app
RUN pip install .
EXPOSE 5000
CMD [ "flaskr" ]
