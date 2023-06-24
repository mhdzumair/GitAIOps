import json
import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from services import services_router

app = FastAPI()
SERVICE_NAME = os.getenv("GITAIOPS_SERVICE_NAME", "gitlab")

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


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def ai_plugin(request: Request):
    """
    This endpoint returns the AI plugin information as a JSON object.
    The information is read from a JSON file and updated with the current host URL and authentication details.
    """
    host_url = str(request.base_url)
    file_path = f"artifacts/.well-known/ai-plugin-{SERVICE_NAME}.json"

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, encoding="utf-8") as json_file:
        plugin_info = json.load(json_file)

    plugin_info.update(
        {
            "legal_info_url": f"{host_url}",
        }
    )
    plugin_info["api"]["url"] = f"{host_url}openapi.json"

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
    """
    This endpoint returns the home page of the API.
    The content is read from an HTML file and returned as an HTML response.
    """
    html_content = Path("artifacts/index.html").read_text(encoding="utf-8")
    return html_content


@app.get("/artifacts/logo.png", include_in_schema=False)
async def read_logo():
    """
    This endpoint returns the logo image file.
    The image is read from the file system and returned as a file response.
    """
    return FileResponse("artifacts/logo.png")
