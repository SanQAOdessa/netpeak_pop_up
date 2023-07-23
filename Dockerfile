FROM joyzoursky/python-chromedriver:3.8

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt

COPY main.py /src

CMD ["python", "main.py"]