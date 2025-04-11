### Setup and running

1. Install requirements:

```sh
python -m pip install -r requirements.txt 
```

2. Add the .env file in the root directory with appropriate environment variables (see .env.sample)

3. Run server:

```sh
python manage.py runserver
```

##### Run tests (optional)

You can run API tests with the next command:

```sh
python manage.py test
```

### Running via docker

1. Please, build the docker image:

```sh
docker build -t meduzzen_be .
```

2. Create and start container

```sh
docker run -p 8000:8000 meduzzen_be
```

##### Run tests (optional)

You can run API tests with the next command:

```sh
docker run -it meduzzen_be python manage.py test
```

### Running via docker compose

1. Please, launch the project:

```sh
docker compose up -d
```

##### Apply migrations

You can apply migrations with the next two lines:

```sh
docker compose run api python manage.py makemigrations
docker compose run api python manage.py migrate
```

##### Run tests (optional)

You can run API tests with the next command:

```sh
docker compose run api python manage.py test
```

### Check the server status using GET request:

```
localhost:8000/api/v1
```
