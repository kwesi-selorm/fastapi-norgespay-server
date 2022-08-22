from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import login, salaries, users
from config import cors_options

app = FastAPI()


app.add_middleware(CORSMiddleware, **cors_options)

app.include_router(login.router)
app.include_router(salaries.router)
app.include_router(users.router)


@app.on_event("startup")
async def start_db():
    try:
        print("Starting database...")
        await init_db()
        print("Database is ready.")
    except Exception:
        print("Couldn't start database")
        raise HTTPException(status_code=500, detail="Connection to the database failed")


# HOME
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the norgesPay FastAPI server!"}
