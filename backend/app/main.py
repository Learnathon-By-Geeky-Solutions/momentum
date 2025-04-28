import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    brand,
    product,
    order,
    profile,
    paybill,
    admin,
)
from app.minio.routers import upload
from app.ai.routers import search

import dotenv
import sentry_sdk


dotenv.load_dotenv()

sentry_sdk.init(
    dsn="https://03bdab86608598f830e7193bd6e4db53@o4508298172497920.ingest.us.sentry.io/4508992259031040",
    send_default_pii=True,
    traces_sample_rate=1.0,
    instrumenter="otel",
)

app = FastAPI(
    title="Handicrafts API Documentation",
    description="API for the Handicrafts application",
    version="1.0.0",
    contact={
        "name": "Team Momentum",
        "url": "https://github.com/Learnathon-By-Geeky-Solutions/momentum",
    },
)

origins = [
    "http://localhost:3001",
    "http://localhost:3000",
    "https://handi-craft.xyz",
    "https://www.handi-craft.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
)



app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(profile.router, prefix="", tags=["Profile"])
app.include_router(brand.router, prefix="", tags=["Brands"])
app.include_router(product.router, prefix="", tags=["Products"])
app.include_router(upload.router, prefix="", tags=["Upload"])
app.include_router(order.router, prefix="", tags=["Orders"])
app.include_router(paybill.router, prefix="", tags=["Paybills"])
app.include_router(search.router, prefix="/search", tags=["Semantic Search"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
