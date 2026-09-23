from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routers import contatos

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")



# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas
app.include_router(contatos.router, prefix="/api")

# frontend
@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()