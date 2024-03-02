FROM python:3
COPY . /usr/app
WORKDIR /usr/app/src/v1
RUN pip3 install -r ../../requirements.txt
EXPOSE 5000
ENV FLASK_ENV=development
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["python3", "app.py"]