import os
import orjson
import uvicorn
import glob
import orjson
from fastapi.responses import HTMLResponse, ORJSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException


def find_path(path):
    """
    Where files are is different depending on the environment, if we're in a
    container search in the /app/src folder, this is pretty quick to search
    from here. Otherwise do a broader search which is a little slower.
    """
    from mabel.logging import get_logger

    logger = get_logger()

    paths = glob.glob(f"**/{path}", recursive=True)
    for i in paths:
        if i.endswith(path):
            logger.info(f"Found `{path}` at `{i}`")
            return i


application = FastAPI(title="Docward")
docs_folder = find_path("docs")
dist_folder = find_path("dist")
templates = Jinja2Templates(directory=find_path("html"))
application.mount("/dist", StaticFiles(directory=find_path("dist")), name="dist")


@application.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    This is a single page app, we deliver a single HTML page and interact
    with the backend using APIs.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@application.get("/v1/docward", response_class=ORJSONResponse)
def home(request: Request):
    paths = glob.glob(f"{docs_folder}/**/*.md", recursive=True)
    paths = [p[len(docs_folder)+1:] for p in paths]
    response = Response(
            orjson.dumps(paths),
            media_type="application/jsonlines",
        )
    return response
    

@application.get("/v1/docward/{page:path}", response_class=HTMLResponse)
def home(page: str):
    from pathlib import Path

    path = Path(f"{docs_folder}/{page}")
    if path.exists():
        with open(path, "r") as file:
            return HTMLResponse(file.read())
    return HTTPException(code=404)

# tell the server to start
if __name__ == "__main__":
    uvicorn.run(
        "docward:application",
        host="0.0.0.0",  # nosec - targetting CloudRun
        port=int(os.environ.get("PORT", 8080)),
        lifespan="on",
    )