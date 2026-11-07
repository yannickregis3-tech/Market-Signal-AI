from fastapi import APIRouter, Query

from app.domain.market import MarketGroup
from app.services.market_catalog import INSTRUMENTS

router = APIRouter(prefix="/markets", tags=["markets"])


@router.get("")
def list_markets(group: MarketGroup | None = Query(default=None)) -> list[dict]:
    instruments = INSTRUMENTS
    if group is not None:
        instruments = [item for item in instruments if item.group == group]
    return [item.model_dump(mode="json") for item in instruments]
