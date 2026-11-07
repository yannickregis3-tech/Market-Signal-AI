# Backend

Python 3.12 / FastAPI service. This first milestone provides a working health API and an explicit market catalogue. It intentionally does not fabricate market prices or trading signals.

## Run locally

Create and activate a virtual environment, then run:

    pip install -e ".[dev]"
    uvicorn app.main:app --reload

Open /docs for interactive API documentation and /health for liveness.

## Optional PostgreSQL dependencies

    pip install -e ".[db,dev]"

Database migrations and persistence repositories will be introduced in the next milestone. Do not place credentials in source control.
