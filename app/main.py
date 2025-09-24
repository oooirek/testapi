import uvicorn
from fastapi import FastAPI

from app.api.v1.router import router as tasks_router
from app.api.v1.router import router_1 as tasks_router_1


app = FastAPI()


app.include_router(tasks_router)
app.include_router(tasks_router_1)







if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)