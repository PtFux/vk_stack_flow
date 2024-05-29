## Enter the PgAdmin 
Some recommends how to use PGAdmin with postgresql in doker-compose _(for me)_
### Enter your password 
`pg_password`
### Register database
Move to **servers-register-server**
#### General
- name: `any`
#### Connection
- Host name/addres: `postgres`
- Port: `5432`
- Maintenance database: `stack_flow_db`
- Username: `flow_user`
- Password: `flow_password`

## Docker-compose
### How to add EnvFile? (in PyCharm)
- Configuration
- Edit
- Docker
- Run
- Modify options
- Environment variables file
- _choose path to our .env_
- _profit!_

### How to use env variable in docker?
> ${POSTGRES_USER:-postgres}

> ${VARIABLE:-default_variable}

```
    env_file:
      - .env
```

### Use PostgresSQL out container
```docker-compose
# docker-compose
    volumes:
      - ./init_db/:/docker-entrypoint-initdb.d
      - ./flow-postgres-data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
```

- В _init_db_ скрипты для создания БД
- Определяем место положение данных в папке _flow-postgres-data_ на хосте
- Определяем трансляцию хоста 5432 контейнера на 5433 хоста


