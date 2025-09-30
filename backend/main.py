from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Apartex API')

app.include_router(auth.router, prefix='/auth', tags=['auth'])

@app.get('/health', tags=['health'])
def health():
    return {'status':'ok'}
