from fastapi import FastAPI
from v1.endpoints import router as router_v1


app = FastAPI()
app.include_router(router=router_v1)
