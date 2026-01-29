from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from domain import model
from adapters import orm, repository
from service_layer import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = FastAPI()


class AddBatchRequest(BaseModel):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None


class AllocateRequest(BaseModel):
    orderid: str
    sku: str
    qty: int


class AllocateResponse(BaseModel):
    batchref: str


@app.post("/add_batch", status_code=201)
def add_batch(request: AddBatchRequest):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    services.add_batch(
        request.ref,
        request.sku,
        request.qty,
        request.eta,
        repo,
        session,
    )
    return "OK"


@app.post("/allocate", response_model=AllocateResponse, status_code=201)
def allocate_endpoint(request: AllocateRequest):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    try:
        batchref = services.allocate(
            request.orderid,
            request.sku,
            request.qty,
            repo,
            session,
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return AllocateResponse(batchref=batchref)
