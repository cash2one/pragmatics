FROM python:3
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt

# setuptools for python 2
RUN wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
		&& python2 get-pip.py "pip==$PYTHON_PIP_VERSION" \
		&& rm get-pip.py

# cloning imdbpy project and installin for python2
RUN git clone https://github.com/alberanid/imdbpy.git \
		&& cd imdbpy \
		&& python2 setup.py --without-lxml --without-cutils --without-sqlalchemy install \
		&& cd ../ \
		&& rm -r imdbpy

CMD ["python", "run.py"]
