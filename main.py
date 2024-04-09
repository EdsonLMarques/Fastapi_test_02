from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
from app.routes import clientes
from app.models.cliente import Cliente
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(clientes.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("clientes.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("cliente_interessado.html", {"request": request})

# Para testes
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI, WebSocket
    from fastapi.websockets import WebSocketDisconnect
    from app.routes import clientes
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from app.routes import clientes
    from fastapi.staticfiles import StaticFiles
    from app.db.models import DadosContato


    app = FastAPI()
    # Configuração para servir arquivos estáticos e templates
    app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
    templates = Jinja2Templates(directory="app/templates")

    #rotas de API
    app.include_router(clientes.router, prefix="/api")

    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        return templates.TemplateResponse("clientes.html", {"request": request})


    @app.get("/dashboard", response_class=HTMLResponse)
    async def read_root(request: Request):
        return templates.TemplateResponse("cliente_interessado.html", {"request": request})


    # WebSocket endpoint para notificar o front-end sobre novos contatos
    from app.routes.clientes import websocket_manager
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket_manager.connect(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            websocket_manager.connections.remove(websocket)

    uvicorn.run(app, host="127.0.0.1", port=8000)