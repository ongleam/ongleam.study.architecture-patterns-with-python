from allocation.domain.model import Batch, OrderLine
from tests.fakes import FakeRepository


class TestFakeRepository:
    def test_can_add_a_batch(self):
        repo = FakeRepository()
        batch = Batch("batch-001", "SMALL-TABLE", 20, eta=None)

        repo.add(batch)

        assert repo.get("batch-001") == batch

    def test_can_retrieve_a_batch(self):
        batch = Batch("batch-001", "RUSTY-FORK", 100, eta=None)
        repo = FakeRepository([batch])

        retrieved = repo.get("batch-001")

        assert retrieved == batch
        assert retrieved.sku == "RUSTY-FORK"

    def test_can_list_batches(self):
        batch1 = Batch("batch-001", "SMALL-TABLE", 20, eta=None)
        batch2 = Batch("batch-002", "LARGE-TABLE", 50, eta=None)
        repo = FakeRepository([batch1, batch2])

        batches = repo.list()

        assert len(batches) == 2
        assert batch1 in batches
        assert batch2 in batches

    def test_allocate_with_fake_repository(self):
        batch = Batch("batch-001", "SMALL-TABLE", 20, eta=None)
        repo = FakeRepository([batch])
        line = OrderLine("order-001", "SMALL-TABLE", 10)

        retrieved = repo.get("batch-001")
        retrieved.allocate(line)

        assert retrieved.available_quantity == 10
