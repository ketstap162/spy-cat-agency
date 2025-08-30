FROM public.ecr.aws/docker/library/python:3.12

ENV PYTHONUNBUFFERED 1;

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]
