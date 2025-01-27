from fastapi import FastAPI
from core.configs import settigns
from api.v1.api import api_router

app: FastAPI = FastAPI(title='Curso API - FastAPI SQLModel')

app.include_router(api_router, prefix=settigns.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
