import uuid
import pytest
from fastapi.testclient import TestClient

from allocation.entrypoints.api import app


client = TestClient(app)


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


@pytest.mark.skip(reason="Requires database setup")
def test_happy_path_returns_201_and_allocated_batch():
    sku = random_sku()
    batchref = random_batchref()
    orderid = random_orderid()

    # TODO: Add batch to database first
    data = {"orderid": orderid, "sku": sku, "qty": 3}

    response = client.post("/allocate", json=data)

    assert response.status_code == 201
    assert response.json()["batchref"] == batchref


@pytest.mark.skip(reason="Requires database setup")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku = random_sku()
    orderid = random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}

    response = client.post("/allocate", json=data)

    assert response.status_code == 400
    assert "Invalid sku" in response.json()["detail"]
