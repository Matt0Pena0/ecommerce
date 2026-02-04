# 🐍 Django Commands (inside Docker)

### EN EL SERVIDOR SIEMPRE PULL ###

```bash
docker compose -f docker-compose.yml up --build

docker compose -f docker-compose.yml exec web python manage.py runscript productos.scripts.load_data 

docker compose -f docker-compose.yml exec web python manage.py migrate

# Run development server on 0.0.0.0:8000
docker compose exec web python3 manage.py runserver 0.0.0.0:8000

# Create new migrations based on model changes
docker compose exec web python3 manage.py makemigrations

# Apply migrations to the database
docker compose -f docker-compose.yml exec web python manage.py migrate

docker compose exec web python3 manage.py migrate

# Create a new app
docker compose exec web python3 manage.py startapp
docker compose --env-file .env.dev -f docker-compose.dev.yml exec web python startapp

# Open Django shell
docker compose exec web python3 manage.py shell

# Open database shell
docker compose exec web python3 manage.py dbshell

# Open database directamente
docker compose exec db mysql -u root -p
docker compose -f docker-compose.dev.yml exec db mysql -u root -p
docker compose --env-file .env.dev -f docker-compose.dev.yml exec db mysql -u root -p

# Create a new Django superuser (admin account)
docker compose exec web python3 manage.py createsuperuser

# LoadData
docker compose --env-file .env.dev -f docker-compose.dev.yml exec web python manage.py loaddata data/backup.json

# DumpData
docker compose -f docker-compose.dev.yml exec web python manage.py dumpdata --format=json --indent=4 --output=backup.json

# Run a custom script (django-extensions)
docker compose exec web python3 manage.py runscript <app>.scripts.<script_name>
docker compose exec web python3 manage.py runscript productos.scripts.load_data 

docker compose -f docker-compose.yml exec web python manage.py runscript productos.scripts.load_data 

# Collect static files into STATIC_ROOT
docker compose exec web python3 manage.py collectstatic --noinput

# Run test suite
docker compose exec web python3 manage.py test
```


# 🐳 Docker Compose

```bash

### Build on prod mode
docker compose -f docker-compose.yml up --build

### Build on dev mode
docker compose --env-file .env.dev -f docker-compose.dev.yml up --build

# Build images and start all services
docker compose up --build

# Start in detached (background) mode
docker compose up -d

# Stop and remove containers, networks and volumes
docker compose down -v

# Stop and remove containers and networks (keep volumes)
docker compose down

# List running containers in this project
docker compose ps

# Stream logs from all services
docker compose logs -f

# Run one-off command inside a service
docker compose exec <service> <command>
# e.g. docker compose exec db mysql -uroot -p<password>

# Run a service temporarily (removes container after exit)
docker compose run --rm <service> <command>
# e.g. docker compose run --rm web python3 manage.py test
```


# 🐳 Docker (standalone)

```bash
# List all containers (running & stopped)
docker ps -a

# List only running containers
docker ps

# Remove a stopped container
docker rm <container_id_or_name>

# Remove an image
docker rmi <image_id_or_name>

# List all volumes
docker volume ls

# Remove a volume
docker volume rm <volume_name>

# Cleanup unused data (containers, images, volumes)
docker system prune -a --volumes

# ver exactamente qué está enviando Docker al construir la imagen:
docker build --no-cache --progress=plain .

# O incluso usar du: ¿?
du -sh * | sort -h
```


# 🔧 Utilities / Debugging

```bash
# Open a bash shell inside the web container
docker compose exec web bash

# Test database connectivity (requires netcat in container)
docker compose exec web nc -z db 3306 && echo "MySQL is up"

# Inspect a Docker network and see connected containers
docker network inspect <network_name>

# Upgrade pip inside the web container
docker compose exec web pip install --upgrade pip
docker compose exec web pip install docutils 0.22

# Rebuild only the web service
docker compose build web

# Remove dangling images and rebuild everything
docker system prune -f && docker compose up --build
```


# Git ([Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary))

| Tipo de commit | Descripción                                          | Ejemplo                                         |
|----------------|------------------------------------------------------| ------------------------------------------------|
| **feat**       | Añade una nueva funcionalidad                        | `feat: Añadir soporte para carrito de compras`  |
| **fix**        | Corrige un error o bug                               | `fix: Corregir error al guardar el carrito`     |
| **perf**       | Mejora el rendimiento                                | `perf: Optimizar la carga de productos`         |
| **refactor**   | Reescribe código sin cambiar su comportamiento       | `refactor: Reestructurar el código del carrito` |
| **docs**       | Modifica la documentación                            | `docs: Actualizar documentación del carrito`    |
| **style**      | Cambios en el estilo (formato, espacios, etc.)       | `style: Formatear el código con Prettier`       |
| **test**       | Añade o corrige pruebas                              | `test: Añadir pruebas para el carrito`          |
| **chore**      | Tareas de mantenimiento (build, dependencias, etc.)  | `chore: Actualizar dependencias`                |
| **ci**         | Cambios en el proceso de integración continua        | `ci: Configurar GitHub Actions para tests`      |
| **build**      | Cambios en el proceso de construcción                | `build: Actualizar el script de construcción`   |
| **rev**        | Reversión de un commit                               | `rev: Revertir commit 'feat: Añadir carrito'`   |
| **wip**        | Trabajo en progreso (Work in Progress)               | `wip: Implementar carrito de compras`           |


## [Modo de Uso](https://www.conventionalcommits.org/en/v1.0.0/#examples)

| Git alias (plugin)                                    | Command                                               |
|-------------------------------------------------------|-------------------------------------------------------|
| g style "remove trailing whitespace"                  | git commit -m "style: remove trailing whitespace"     |
| g wip -a "work in progress"                           | git commit -m "wip!: work in progress"                |
| g fix -s "router" "correct redirect link"             | git commit -m "fix(router): correct redirect link"    |
| g rev -s "api" "rollback v2"                          | git commit -m "revert(api): rollback v2"              |


*sintaxis:* `g <type>  [-s "<scope>"] [-a] "<message>"`

*sintaxis:* `g style -s "navbar" -a "Cambiando color"`
