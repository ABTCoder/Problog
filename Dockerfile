FROM python:3.7

MAINTAINER IA 2020/2021

EXPOSE 8000

#install dependencies
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#Run the code

CMD ["python3 webapp.py"]