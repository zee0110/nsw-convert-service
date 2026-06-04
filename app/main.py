"""A small FastAPI conversion microservice.

Demonstrates a clean service with strong typing, error handling, and a CI/CD
pipeline (lint + test + coverage + Docker build) in GitHub Actions.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import conversions

app = FastAPI(
    title="Convert Service",
    version="1.0.0",
    description="Length, mass, temperature, and (illustrative) currency conversion microservice.",
)


class ConvertRequest(BaseModel):
    value: float = Field(..., examples=[100.0])
    from_unit: str = Field(..., examples=["km"])
    to_unit: str = Field(..., examples=["mi"])


class ConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float


_DISPATCH = {
    "length": conversions.convert_length,
    "mass": conversions.convert_mass,
    "temperature": conversions.convert_temperature,
    "currency": conversions.convert_currency,
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/convert/{kind}", response_model=ConvertResponse)
def convert(kind: str, req: ConvertRequest) -> ConvertResponse:
    func = _DISPATCH.get(kind)
    if func is None:
        raise HTTPException(404, detail=f"Unknown conversion kind '{kind}'. "
                                        f"Try: {', '.join(_DISPATCH)}.")
    try:
        result = func(req.value, req.from_unit, req.to_unit)
    except conversions.ConversionError as e:
        raise HTTPException(400, detail=str(e)) from e
    return ConvertResponse(
        value=req.value, from_unit=req.from_unit, to_unit=req.to_unit, result=round(result, 6)
    )
