# Plataforma E-Commerce con Django y Docker

> Una plataforma de e-commerce full-stack desplegada en un entorno de producción contenerizado, intentando seguir las mejores prácticas de DevOps.

Este proyecto demuestra el ciclo de vida completo del desarrollo de una aplicación web, desde la configuración inicial del código hasta el despliegue final en producción.

## ✨ Stack Tecnológico

* **Backend:** Python, Django
* **Base de Datos:** MySQL
* **Frontend:** HTML, SCSS, Bootstrap 5, NPM
* **Infraestructura:** Docker, Docker Compose, Nginx (como Proxy Inverso), VPS (Ubuntu)

## 🚀 Características Principales

* Gestión de Productos.
* Sistema de Autenticación de Usuarios (Registro, Login, Cambio y recuperación de Contraseña).
* Carrito de Compras funcional, asíncrono y con una interfaz mínimamente agradable.
* Creación y visualización de Órdenes de Compra.
* Estructura que permite mejoras y nuevas funcionalidades.

## ⚙️ Arquitectura de Despliegue (DevOps)

El núcleo de este proyecto es la implementación de un flujo de trabajo DevOps:

* **Contenerización:** La aplicación Django (con Gunicorn) y la base de datos MySQL corren en contenedores Docker aislados, orquestados con Docker Compose.
* **Proxy Inverso:** Nginx se ejecuta en el servidor anfitrión, gestionando el tráfico público, sirviendo archivos estáticos de forma eficiente y redirigiendo las peticiones dinámicas a la aplicación Django.
* **Seguridad:**
    * Implementación de HTTPS con certificados SSL gestionado por Certbot.
    * Acceso al servidor securizado mediante llaves SSH (deshabilitando contraseñas) El acceso está restringido por un doble firewall (UFW y a nivel de proveedor).
    * Se utiliza Tailscale para crear una red privada virtual (VPN), permitiendo el acceso SSH a través de una IP interna y estable. Esto elimina la necesidad de exponer puertos al público y me ayudo a resolver por completo el problema, tan molesto, de las IPs dinámicas.
    * Gestión de secretos y configuraciones de entorno a través de archivos `.env`.
* **Build de Frontend:** Se utiliza un `Dockerfile` multi-etapa que compila los assets de SASS usando un contenedor de Node.js, optimizando la imagen de producción final, a modo de prueba y aprendizaje de por medio, en bootstrap.
* **Flujo de Trabajo Git:** Se sigue un modelo Git-Flow simplificado con ramas `main` (producción), `dev` (desarrollo) y `feature` (nuevas funcionalidades). 
    Se sigue un modelo Git-Flow simplificado con ramas main (producción), dev (desarrollo) y feature (nuevas funcionalidades). Durante el despliegue inicial, me encontré con dificultades, perdiendo las buenas prácticas que intentaba seguir.

    Un archivo .env con secretos se filtró accidentalmente al repositorio, lo que motivó una limpieza profunda del historial utilizando la herramienta BFG Repo-Cleaner (a pesar de ser un proyecto de aprendizaje, fue una buena excusa para intentar aprender del error, y pensar en las consecuencias). A esto se sumó el desafío de gestionar por primera vez Git en un VPS y el proceso de despliegie en sí.

    Lejos de ser un error catastrófico, fue una valiosa oportunidad de aprendizaje que sentó las bases para futuros proyectos.

## 🛠️ Instalación y Uso Local

1.  Clonar el repositorio: `git clone [URL]`
2.  Crear y configurar el archivo de entorno de desarrollo: `cp .env.example .env.dev`
3.  Levantar los contenedores: `docker compose up --build`
4.  La aplicación estará disponible en `http://localhost:8000`.
