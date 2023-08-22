from fastapi import FastAPI
from routers import user, auth, follow

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(follow.router)

@app.get("/")
def hello_world():
    return {"message": "hello world"}