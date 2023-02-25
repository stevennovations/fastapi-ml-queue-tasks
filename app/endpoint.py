from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from utils import config
from utils.redis import init_redis_pool
from router import forecast_router
from utils.log_config import get_logger

description = """
Forecasting API helps you assess the demand for a particular date. 🚀

## Forecast Date

You will be able to:

* **Get demand for specific date** (_not implemented_).
"""

logger = get_logger(__name__)
global_settings = config.Settings()
app = FastAPI(title='nike-forecasting-app',
              docs_url='/api/v1/nikesalesforecast/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(forecast_router, prefix='/api/v1/nikesalesforecast')


@app.on_event("startup")
async def startup_event():
    logger.info("Opening mols bakery...")
    app.state.redis = await init_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Closing mols bakery...")
    await app.state.redis.close()


@app.get("/health-check")
async def health_check(settings: config.Settings = Depends(config.get_settings)
                       ):
    try:
        await app.state.redis.set(str(settings.redis_url), settings.up)
        value = await app.state.redis.get(str(settings.redis_url))
    except Exception:  # noqa: E722
        logger.exception("Sorry no power we can't open bakery...")
        value = settings.down
    return {settings.web_server: settings.up, str(settings.redis_url): value}
