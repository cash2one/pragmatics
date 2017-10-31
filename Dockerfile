FROM python:3
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt
CMD ["python", "run.py"]

#py -2.7 -m pip install imdb
