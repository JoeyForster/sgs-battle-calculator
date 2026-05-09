from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from .engine import simulate_battle
from .example import EXAMPLE_BATTLE
from .models import BattleInput


PACKAGE_DIR = Path(__file__).resolve().parent
STATIC_DIR = PACKAGE_DIR / "static"

app = FastAPI(title="SGS Battle Calculator", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


@app.get("/api/example")
def get_example() -> dict[str, Any]:
    return EXAMPLE_BATTLE


@app.post("/api/validate")
async def validate_battle(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
        BattleInput.model_validate(payload)
    except ValidationError as exc:
        return JSONResponse({"valid": False, "errors": exc.errors()})
    except Exception as exc:
        return JSONResponse({"valid": False, "errors": [{"msg": str(exc)}]})
    return JSONResponse({"valid": True, "errors": []})


@app.post("/api/simulate")
def simulate(payload: BattleInput) -> dict[str, Any]:
    return simulate_battle(payload).model_dump(mode="json")
