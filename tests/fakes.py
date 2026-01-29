from allocation.domain import model
from allocation.adapters.repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list[model.Batch] | None = None):
        self._batches = set(batches) if batches else set()

    def add(self, batch: model.Batch):
        self._batches.add(batch)

    def get(self, reference: str) -> model.Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[model.Batch]:
        return list(self._batches)
