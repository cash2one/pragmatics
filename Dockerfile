FROM python:3
WORKDIR /code
ADD . /code

RUN pip install -r requirements.txt

# setuptools for python 2
RUN wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
		&& python2 get-pip.py "pip==$PYTHON_PIP_VERSION" \
		&& rm get-pip.py

# git clone https://github.com/alberanid/imdbpy.git \
RUN cd imdbpy \
		&& python2 setup.py --without-lxml --without-cutils --without-sqlalchemy install \
		&& cd ../
#		&& rm -r imdbpy

EXPOSE 80

CMD ["python", "run.py"]
