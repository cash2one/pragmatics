FROM python:3
WORKDIR /code
ADD . /code
RUN pip3 install -r requirements.txt

#RUN apt-get update && apt-get install -y \
#    python2.7 \

FROM python:2.7
RUN pip2 install -r requirements2.txt
#CMD ["py", "-2.7", "-m", "pip", "install", "imdb"]
#RUN py -2.7 -m pip install imdb

CMD ["python3", "run.py"]

#py -2.7 -m pip install imdb
