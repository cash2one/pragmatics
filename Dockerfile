FROM python:3
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt
CMD ["python", "run.py"]