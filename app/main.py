from fastapi import FastAPI
from .routes import tasks, auth

app = FastAPI(title='Task Manager')

app.include_router(tasks.router, prefix='/tasks', tags=['Tasks'])
app.include_router(auth.router, prefix='/auth', tags=['Auth'])


@app.get('/')
async def index():
    return {'message': 'Welcome to the web-task-manager!'}
