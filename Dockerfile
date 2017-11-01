#FROM python:2.7
#WORKDIR /code
#ADD . /code
#RUN pip install -r requirements2.txt

FROM python:3
WORKDIR /code
ADD . /code
RUN pip3 install -r requirements.txt

CMD ["python", "run.py"]

#RUN python2 imdb_connection.py "James Bond"
#py -2.7 -m pip install imdb
