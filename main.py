from fastapi import FastAPI
from api.v1.endpoints import router as router_v1


app = FastAPI()
app.include_router(router=router_v1)
