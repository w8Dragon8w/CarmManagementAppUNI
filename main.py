from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from routes import garages, cars, maintenance

app=FastAPI()

@app.get("/info")
def info():
    return{"version": "0.1"}

@app.get("/")
def home():
    return {"message": "Home page, test"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(garages.router, prefix="/garages", tags=["Garages"])
app.include_router(cars.router, prefix="/cars", tags=["Cars"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenances"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)