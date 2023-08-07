from fastapi import FastAPI

from .routers import user, event, auth, profile

app = FastAPI()

app.include_router(event.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(profile.router)


@app.get('/')
async def root():
    return {"welcome": "Hello! This is ITET Project."}
