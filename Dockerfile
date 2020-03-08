FROM python:alpine3.7
COPY dist/*.whl /app
#ARGS


#ENV
ENV
WORKDIR /app
RUN pip install .
EXPOSE 5000
CMD [ "flaskr" ]
