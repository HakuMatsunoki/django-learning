## Meduzzen API

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

4. Please, check the server status using GET request:

```
localhost:8000/api/v1
```

##### Run tests (optional)

You can run API tests with the next command:

```sh
python manage.py test
```

