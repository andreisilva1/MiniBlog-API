from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import master_router
from app.database.session import create_db_tables
from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler, 
              contact={
            "name": "Andrei Silva",
            "url": "https://github.com/andreisilva1",
            "email": "andrei.pydev@gmail.com"}
        )
app.include_router(master_router)


@app.get("/", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="MiniBlog API")
