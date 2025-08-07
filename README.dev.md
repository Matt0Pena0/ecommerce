# 🐍 Django Commands (inside Docker)

```bash
# Run development server on 0.0.0.0:8000
docker compose exec web python3 manage.py runserver 0.0.0.0:8000

# Create new migrations based on model changes
docker compose exec web python3 manage.py makemigrations

# Apply migrations to the database
docker compose exec web python3 manage.py migrate

# Create a new app
docker compose exec web python3 manage.py startapp

# Open Django shell
docker compose exec web python3 manage.py shell

# Open database shell
docker compose exec web python3 manage.py dbshell

# Create a new Django superuser (admin account)
docker compose exec web python3 manage.py createsuperuser

# Run a custom script (django-extensions)
docker compose exec web python3 manage.py runscript <app>.scripts.<script_name>

# Collect static files into STATIC_ROOT
docker compose exec web python3 manage.py collectstatic --noinput

# Run test suite
docker compose exec web python3 manage.py test
```

# 🐳 Docker Compose

```bash
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

