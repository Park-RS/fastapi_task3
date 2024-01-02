import uvicorn
from fastapi import FastAPI
from public.books import router
from database import create_async_tables, init_db

app = FastAPI()
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await init_db()
    await create_async_tables()



# @app.on_event("shutdown")
# def shutdown_event():
#     with open("log.txt", mode="a") as log:
#         log.write("Application shutdown")

@app.get("/")
async def main():
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
