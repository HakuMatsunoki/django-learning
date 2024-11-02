FROM python:3.12.7-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /meduzzen_be

COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x ./start.sh

CMD ["./start.sh"]
