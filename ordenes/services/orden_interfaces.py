from typing import Protocol


class IOrdenesService(Protocol):
    def crear_orden(self, usuario, items): ...