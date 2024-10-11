from fastapi import FastAPI
from .routes import tasks, users

app = FastAPI(title='Task Manager')

app.include_router(tasks.router, prefix='/tasks', tags=['Tasks'])
app.include_router(users.router, prefix='/users', tags=['Users'])


@app.get('/')
async def index():
    return {'message': 'Welcome to the web-task-manager!'}
