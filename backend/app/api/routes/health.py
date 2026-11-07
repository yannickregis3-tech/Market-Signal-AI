from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Service liveness")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "market-signal-ai"}
