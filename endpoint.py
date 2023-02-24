from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router

description = """
Forecasting API helps you assess the demand for a particular date. 🚀

## Forecast Date

You will be able to:

* **Get demand for specific date** (_not implemented_).
"""

app = FastAPI(docs_url='/api/v1/nikesalesforecast/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router, prefix='/api/v1/nikesalesforecast')