from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation import config
from allocation.domain import model
from allocation.adapters import orm, repository
from allocation.service_layer import services


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = FastAPI()


class AllocateRequest(BaseModel):
    orderid: str
    sku: str
    qty: int


class AllocateResponse(BaseModel):
    batchref: str


class ErrorResponse(BaseModel):
    message: str


@app.post("/allocate", response_model=AllocateResponse, status_code=201)
def allocate_endpoint(request: AllocateRequest):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.orderid, request.sku, request.qty,
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return AllocateResponse(batchref=batchref)
