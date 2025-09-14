from fastapi import FastAPI


from database import create_tables, drop_tables

from contextlib import asynccontextmanager
from router import router as tasks_router



# взято из доки и кст я не знаю че это
@asynccontextmanager
async def lifespan(app: FastAPI):
    await  drop_tables()
    print("база очищена")
    # load the ml model
    await create_tables()
    print("база готова")
    yield
    #clean up the ml models and release the resources
    print("выключение")



app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

