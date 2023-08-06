from fastapi import FastAPI

from .routers import user, post, auth

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {"welcome": "Hello! This is ITET Project."}
