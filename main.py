from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controller import user, note

app = FastAPI()


app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(note.router, prefix="/notes", tags=["notes"])

@app.get("/")
async def index():
    return {"message": "Hello World"}

origins = [
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)