FROM python:3
COPY . /usr/src/app
WORKDIR /user/src/app/src/v1
RUN pip3 install -r ../../requirements.txt
CMD ["flask", "run"]