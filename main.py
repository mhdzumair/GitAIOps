import json
import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from services import services_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("gql.transport.aiohttp").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Add routes from each service
app.include_router(services_router, prefix="/services")

# Serve static files from the /artifacts directory at the root of the domain
app.mount("/artifacts", StaticFiles(directory="artifacts"), name="artifacts")

SERVICE_NAME = os.getenv("GITAIOPS_SERVICE_NAME", "gitlab")


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def ai_plugin(request: Request):
    host_url = str(request.base_url)
    file_path = f"artifacts/.well-known/ai-plugin-{SERVICE_NAME}.json"

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, encoding="utf-8") as json_file:
        plugin_info = json.load(json_file)

    plugin_info.update(
        {
            "logo_url": f"{host_url}artifacts/logo.png",
            "legal_info_url": f"{host_url}",
            "api": {"url": f"{host_url}openapi.json"},
        }
    )

    if "localhost" in host_url or "127.0.0.1" in host_url:
        plugin_info["auth"] = {"type": "none"}
        plugin_info["name_for_human"] += " Local"
        plugin_info["name_for_model"] += "_local"
    else:
        plugin_info["auth"]["verification_tokens"]["openai"] = os.getenv(
            "OPENAI_PLUGIN_VERIFICATION_TOKEN"
        )

    return plugin_info


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_home():
    html_content = Path("artifacts/index.html").read_text(encoding="utf-8")
    return html_content
