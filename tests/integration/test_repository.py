from allocation.domain import model
from allocation.adapters import repository


def test_get_by_batchref(session):
    repo = repository.SqlAlchemyRepository(session)
    b1 = model.Batch(ref="batch1", sku="sku1", qty=100, eta=None)
    b2 = model.Batch(ref="batch2", sku="sku1", qty=100, eta=None)
    b3 = model.Batch(ref="batch3", sku="sku2", qty=100, eta=None)
    p1 = model.Product(sku="sku1", batches=[b1, b2])
    p2 = model.Product(sku="sku2", batches=[b3])
    repo.add(p1)
    repo.add(p2)
    assert repo.get_by_batchref("batch2") == p1
    assert repo.get_by_batchref("batch3") == p2
