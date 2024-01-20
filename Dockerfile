FROM python:3
COPY . /usr/app
WORKDIR /usr/app/src/v1
RUN pip3 install -r ../../requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]