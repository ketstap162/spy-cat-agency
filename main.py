import multiprocessing

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.core.settings import settings
from api.routes import main_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

max_workers_count = multiprocessing.cpu_count() * 2 + 1


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level="info",
        reload=True,
        workers=max_workers_count,
    )
