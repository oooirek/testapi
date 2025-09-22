import uvicorn
from fastapi import FastAPI
from app.db.database import init_db
from app.api.v1.router import router as tasks_router



app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()



app.include_router(tasks_router)








if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)