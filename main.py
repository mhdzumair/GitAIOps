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

# Add routes from each service
app.include_router(services_router, prefix="/services")

# Serve static files from the /artifacts directory at the root of the domain
app.mount("/artifacts", StaticFiles(directory="artifacts"), name="artifacts")

SERVICE_NAME = os.getenv("GITAIOPS_SERVICE_NAME", "gitlab")


@app.get("/.well-known/ai-plugin.json")
async def ai_plugin(request: Request):
    host_url = str(request.base_url)
    file_path = f"artifacts/.well-known/ai-plugin-{SERVICE_NAME}.json"

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path) as json_file:
        plugin_info = json.load(json_file)
        plugin_info["logo_url"] = f"{host_url}artifacts/logo.png"
        plugin_info["legal_info_url"] = f"{host_url}"
        plugin_info["api"]["url"] = f"{host_url}openapi.json"
        if "localhost" in host_url or "127.0.0.1" in host_url:
            plugin_info["auth"] = {"type": "none"}
        else:
            plugin_info["auth"]["verification_tokens"]["openai"] = os.getenv(
                "OPENAI_PLUGIN_VERIFICATION_TOKEN"
            )

    return plugin_info


@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = Path("artifacts/index.html").read_text()
    return html_content
