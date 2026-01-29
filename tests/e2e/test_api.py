import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from allocation import config
from allocation.adapters.orm import metadata, start_mappers
from allocation.entrypoints.api import app


@pytest.fixture(scope="module")
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    session = sessionmaker(bind=postgres_db)()
    yield session
    session.close()


@pytest.fixture
def add_stock(postgres_session):
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            postgres_session.execute(
                text(
                    "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
                    " VALUES (:ref, :sku, :qty, :eta)"
                ),
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            result = postgres_session.execute(
                text("SELECT id FROM batches WHERE reference=:ref AND sku=:sku"),
                dict(ref=ref, sku=sku),
            )
            batch_id = result.fetchone()[0]
            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(
            text("DELETE FROM allocations WHERE batch_id=:batch_id"),
            dict(batch_id=batch_id),
        )
        postgres_session.execute(
            text("DELETE FROM batches WHERE id=:batch_id"),
            dict(batch_id=batch_id),
        )
    for sku in skus_added:
        postgres_session.execute(
            text("DELETE FROM order_lines WHERE sku=:sku"),
            dict(sku=sku),
        )
    postgres_session.commit()


client = TestClient(app)


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


def test_happy_path_returns_201_and_allocated_batch(add_stock):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref("1")
    laterbatch = random_batchref("2")
    otherbatch = random_batchref("3")
    add_stock(
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, othersku, 100, None),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}

    response = client.post("/allocate", json=data)

    assert response.status_code == 201
    assert response.json()["batchref"] == earlybatch


def test_unhappy_path_returns_400_and_error_message():
    unknown_sku = random_sku()
    orderid = random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}

    response = client.post("/allocate", json=data)

    assert response.status_code == 400
    assert "Invalid sku" in response.json()["detail"]
