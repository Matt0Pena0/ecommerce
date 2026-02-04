from locust import HttpUser, task, between
import random

LISTA_IDS = list(range(100))

class UsuarioSPA(HttpUser):
    # Tiempo de espera entre peticiones
    wait_time = between(1, 4)

    def on_start(self):
        """
        Login:
        """
        # 1. GET para obtener la cookie CSRF
        response = self.client.get("/accounts/login/")
        token_anonimo = self.client.cookies.get("csrftoken")

        # 2. POST para loguearse
        self.client.post(
            "/accounts/login/",
            data={
                "username": "admin2",
                "password": "1234",
                "csrfmiddlewaretoken": token_anonimo,
            },
            headers={"Referer": "/accounts/login/"}
        )

        self.csrf_token = self.client.cookies.get("csrftoken")


    @task(5)
    def listar_productos(self):
        """
        Carga primero el HTML vacío y luego llama a la API.
        """
        # Carga el App Shell
        self.client.get("/productos/listar/", name="PAGE: Listado HTML")
        
        # Carga los Datos JSON
        self.client.get("/api/productos/", name="API: Listar Productos")

    @task(3)
    def agregar_al_carrito(self):
        """
        Usa el ViewSet de Carrito de DRF.
        """
        if not LISTA_IDS: return
        p_id = random.choice(LISTA_IDS)
        
        # Simula agregar entre 1 y 3 unidades
        self._api_carrito_action(p_id, random.randint(1, 3), name="API: Agregar Carrito")

    @task(2)
    def ajustar_stepper(self):
        """
        Simula el uso de los botones +/- del stepper.
        En tu nueva API, esto probablemente usa el mismo endpoint de actualización.
        """
        if not LISTA_IDS: return
        p_id = random.choice(LISTA_IDS)
        # Simula un cambio de cantidad
        self._api_carrito_action(p_id, random.randint(1, 5), name="API: Update Cantidad")

    @task(1) 
    def finalizar_compra(self):
        """
        Simula al usuario que decide comprar.
        """
        with self.client.get("/carrito/finalizar/", catch_response=True, name="PAGE: Checkout") as response:
            if response.status_code in [200, 301, 302]:
                response.success()
            else:
                # Ignora 404 si el carrito está vacío
                if response.status_code == 404:
                    response.success() 
                else:
                    response.failure(f"Fallo checkout: {response.status_code}")

    def _api_carrito_action(self, producto_id, cantidad, name):
        """
        Helper para comunicarse con DRF
        """
        # Headers necesarios para DRF
        headers = {
            "X-CSRFToken": self.csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
        }

        payload = {"producto_id": producto_id, "cantidad": cantidad}

        self.client.post(f"/api/carrito/agregar/", json=payload, headers=headers, name=name)
