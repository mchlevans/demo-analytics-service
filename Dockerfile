# FROM python:3
FROM python:3.12.2-slim-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY ./scripts/install.sh ./
RUN chmod 777 ./install.sh 
RUN ./install.sh

ADD src/ ./src/

RUN cd src && ls 

# need to make port variable
EXPOSE 8000

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "src.app:app()" ]
