from typing import Protocol


class IExporter(Protocol):
    def export(self, rows: list[dict]) -> bytes:
        ...
