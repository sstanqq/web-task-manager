from fastapi import FastAPI

app = FastAPI(title='Task Manager')


@app.get('/')
async def index():
    return {'message': 'Welcome to the web-task-manager!'}
