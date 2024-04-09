# Backend API

  <img src="https://shields.io/badge/python-^3.10-3776AB?logo=python&style=for-the-badge&logoColor=white" alt="python">
  <img src="https://shields.io/badge/fastapi-^0.103.2-009688?logo=fastapi&style=for-the-badge&logoColor=white" alt="fastapi">
  <img src="https://shields.io/badge/sqlachemy-^2.0.10-D71F00?logo=websockets&style=for-the-badge&logoColor=white" alt="websockets">
  <img src="https://shields.io/badge/postgresql-14.0-4169E1?logo=postgresql&style=for-the-badge&logoColor=white" alt="websockets">
  <img src="https://shields.io/badge/alembic-^1.7.4-2D9FD9?logo=postgresql&style=for-the-badge&logoColor=white" alt="websockets">
  <img src="https://shields.io/badge/pydantic-2.0.0-E92063?logo=pydantic&style=for-the-badge&logoColor=white" alt="websockets">

## Instalation

- Install Postgressql
  - Some Linux distros (like Ubuntu) might not have the package in the repositories, in that case you should follow the postgres documentation:
    https://www.postgresql.org/download/linux
  - When you have the package run
    ```commandline
    sudo apt update
    sudo apt install postgresql-12
    ```
  - Change to the default user of postgres
    ```commandline
    sudo su postgres
    ```
  - Enter sql cmd
    ```commandline
    psql
    ```
  - Create a new database
    ```commandline
    CREATE DATABASE database_name;
    ```
  - Change user authentication type to password
    ```commandline
    ALTER USER 'username' password 'new_pasword';
    ```
  - Save the connectionstring, it should be something like
    ```commandline
    postgresql://DB_USER_NAME:DB_USER_PASS@IP_DB:PORT_DB/DATABSE_NAME
    ```
- Donwload the project
  ```commandline
   git clone https://github.com/wygame-io/api
  ```
- Create a .env file with the folowing variables:
  ```env
  DATABSE_URL=CONNECTION_STRING
  SECRET=SECRET_STRING
  ORIGINS=URL1,URL2,URL3,...
  PUBLIC_KEY_SECRET=NUMBER1,NUMBER2
  PRIVATE_KEY_SECRET=NUMBER1,NUMBER2,NUMBER3,NUMBER4,NUMBER5
  MAIL_USERNAME=USERNAME
  MAIL_PASSWORD=PASSWORD
  MAIL_FROM=mail@example.abc
  MAIL_PORT=PORT_NUMBER
  MAIL_SERVER=(EXEMPLO)smtp.mailtrap.io
  MAIL_TLS=TRUE_OR_FALSE
  MAIL_SSL=TRUE_OR_FALSE
  ```
  - Explanation of the .env variables:
  ```
  DATABSE_URL: Conection String to connect to the database
  SECRET: Long String to use as a Key to encrypt the JWT tokens
  ORIGINS: URLs whitelisted to bypass the CORS error
  PUBLIC_KEY_SECRET: Public Key for the encryption of the Payment Token
  PRIVATE_KEY_SECRET: Private Key for the encryption of the Payment Token
  MAIL_USERNAME: Username of the email account used by the server
  MAIL_PASSWORD: Password of the email account used by the server
  MAIL_FROM: Email string of the email account used by the server
  MAIL_PORT: Email port of the email account used by the server
  MAIL_SERVER: Server of the email account used by the server
  MAIL_TLS: If the server should use TLS in the emails
  MAIL_SSL: If the server should use SSL in the emails
  ```
  - To get the Number for the private keys do the following:
    ```commandline
    pip install rsa
    python3
    rsa.newkeys(number_of_bits_desired)
    ```
    It will output something like:
    ```commandline
    (PublicKey(NUMBER1, NUMBER2), PrivateKey(NUMBER1, NUMBER2, NUMBER3, NUMBER4, NUMBER5))
    ```
    Then it's just needed to copy the keys to the .env file, be carefull to not let any spaces between then nor the class name nor the "()".
- After that run the following commands in the project's root directory:
  ```commandline
  pipenv install
  pipenv shell
  ```
- Create the database's tables:
  ```commandline
  alembic upgrade head
  ```
- Start the project:
  ```commandline
   uvicorn main:app --reload
  ```

## Add a new migration to the database

```commandline
 alembic revision --autogenerate -m "Revision message"
 alembic upgrade head
```

## Start the Local Server

```commandline
cd /path/to/folder/api && poetry shell
```

Then when the env shell is open run:

```commandline
uvicord app:app --reload
```

Or if you want to specify an address (useful to access the local server with other devices (for example a phone to test responsiveness))

```commandline
uvicord app:app --reload --host="X.X.X.X"
```

## Other relevant info

- The application when deployed in the Heroku give an error because the connection to the database were superior that the max allowed for the billing plan (20). To resolve that was added a new buildpack with the command:
  ```commandline
  heroku buildpacks:add https://github.com/heroku/heroku-buildpack-pgbouncer -a pepe-api-staging
  ```
- Then the procfile was modified too:

  ```commandline
  web: bin/start-pgbouncer-stunnel uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
  ```

  - In the future may be wise to remove this in case the billing plan allows more connections

- Add change to heroku without automatic deploys:

  ```commandline
  git push heroku:master
  ```

- See logs of the application:
  ```commandline
  heroku logs --tail -a kempo-api-staging
  heroku logs --tail -n 500 -a kempo-api-staging
  ```
  - "-n 5000" refers to the number of lines to see

## Usefull Alias

- Start the enviroment shell:
  ```commandline
  alias api="cd /directory/to/project/api && poetry shell"
  ```
- Start the local server:
  ```commandline
  alias uvi="uvicord app:app --reload --host="X.X.X.X""
  ```
