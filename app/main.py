import uvicorn
from fastapi import FastAPI

from app.api.v1.router import router as tasks_router
from app.api.v1.router import router_1 as tasks_router_1
from app.auth.routes import router as auth_router

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Mini Jira")

origins = [
    "http://localhost:5500",  # адрес фронтенда
    "http://127.0.0.1:5500",
    "*",  # временно можно для теста разрешить все    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tasks_router)
app.include_router(tasks_router_1)
app.include_router(auth_router)




if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)