import json
import os.path
import subprocess
import time
import traceback
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from importlib_resources import files
from pydantic import BaseModel, Extra

from digital_twin_distiller.ml_project import MachineLearningProject
from digital_twin_distiller.modelpaths import ModelDir
from digital_twin_distiller.simulationproject import SimulationProject


class InputJsonML(BaseModel):
    """
    Class for validating the input sent to the /process endpoint for MachineLearningProject.
    """

    text: str

    # Setting for keeping the additional keys in the input json intact
    class Config:
        extra = Extra.allow


class InputJsonSim(BaseModel):
    """
    Class for validating the input sent to the /process endpoint for SimulationProject.
    """

    simulation: Optional[dict] = {"type": "default"}
    model: Optional[dict] = {}
    tolerances: Optional[dict] = {
        "type": "ff",
        "parameters": {},
        "variables": [],
    }
    misc: Optional[dict] = {"processes": 4, "cleanup": True, "exportname": None}
    # TODO: get this version number from poetry, what do we want from this version
    version: Optional[str] = "2021.12"

    # Setting for keeping the additional keys in the input json intact
    class Config:
        extra = Extra.allow


# Defining the API
app = FastAPI(title="{} API", docs_url="/apidocs", redoc_url=None)

tags_metadata = [
    {
        "name": "process_ml",
        "description": "Run project on a single document sent for the API.",
        "externalDocs": {
            "description": "Find out more",
            "url": "http://montana.ai",
        },
    },
    {
        "name": "process_sim",
        "description": "Run simulations for the API.",
        "externalDocs": {
            "description": "Find out more",
            "url": "http://montana.ai",
        },
    },
    {"name": "ping", "description": "Endpoint for pinging server."},
    {
        "name": "docs",
        "description": "Endpoint for OpenAPI documentation.",
        "externalDocs": {
            "description": "Find out more",
            "url": "http://montana.ai",
        },
    },
    {
        "name": "root",
        "description": "Test page for the API. Endpoint called by the main page of the API test page.",
    },
    {"name": "docs", "description": "Endpoint for the project documentation."},
]


@app.post("/process_sim", include_in_schema=True, tags=["process_sim"])
async def process_sim(item: InputJsonSim):
    """
    Endpoint for performing the project.run() method on data sent for the API in JSON format.
    The endpoint performs automatic input validation via the Item class.
    """
    data = json.loads(item.json())
    app.project._output.clear()
    try:
        app.project._input = data
        app.project.update_input()
        app.project.run()
    except Exception as e:
        app.project._output["exception"] = {
            "type": e.__class__.__name__,
            "message": str(e),
            "traceback": traceback.format_exc(),
        }
    finally:
        return app.project._output


@app.post("/process_ml", include_in_schema=True, tags=["process_ml"])
async def process_ml(item: InputJsonML):
    """
    Endpoint for performing the project.run() method on data sent for the API in JSON format.
    The endpoint performs automatic input validation via the Item class.
    """
    data = json.loads(item.json())
    if data:
        app.project.add_single_input(data)
        app.project.run()
    return app.project.get_single_output()


@app.get("/ping", include_in_schema=True, tags=["ping"])
def ping():
    """
    Pings the server to check if it is available.
    """
    result_json = {}
    result_json["call_time"] = time.ctime()
    result_json["msg"] = "The API is working."
    return result_json


@app.get("/", include_in_schema=True, tags=["docs"])
def project_documentation(request: Request):
    """
    Endpoint for checking the custom project's documentation.
    """
    return app.doc_templates.TemplateResponse("index.html", {"request": request, "project_name": app.project.app_name})


class Encapsulator:
    """
    Server for running a custom project as an API.
    """

    def __init__(self, project):
        """
        :param project: either MachineLearningProject or SimulationProject instance
        """
        self.app = app
        self.app.doc_templates = Jinja2Templates(
            directory=files("digital_twin_distiller") / "resources" / "doc_template" / "site"
        )
        self.app.project = project
        self.app.title = self.app.title.format(project.app_name)
        # self.workers = self.number_of_workers()
        self.host = "127.0.0.1"
        self.port = 5000
        self.cert_file_path = None
        self.key_file_path = None

        self.set_project_mkdocs_dir_path(ModelDir.DOCS)

    def set_cert_file_path(self, cert_file_path):
        self.cert_file_path = cert_file_path

    def set_key_file_path(self, key_file_path):
        self.key_file_path = key_file_path

    def set_project_mkdocs_dir_path(self, mkdocs_path):
        r"""
        The function shows an mk-docs documentation under the /docs Endpoint.

        The function waits for the mk-docs documentation project's folder and shows to the \site page where is the
        mkdocs path can be set. The \site page is generated by the >build mkdocs command

        :path mkdocs_path:
        """
        mkdocs_path = os.path.join(mkdocs_path, "site")
        self.app.doc_templates = Jinja2Templates(directory=mkdocs_path)

        asset_path = os.path.join(mkdocs_path, "assets")
        search_path = os.path.join(mkdocs_path, "search")
        # javascripts_path = os.path.join(asset_path, "javascripts")
        # worker_path = os.path.join(javascripts_path, "workers")
        if not os.path.exists(asset_path) or not os.path.exists(search_path):
            raise FileNotFoundError('please build the mkdocs site by calling "mkdocs build" in the docs directory')

        self.app.mount("/assets", StaticFiles(directory=asset_path), name="assets")
        self.app.mount("/search", StaticFiles(directory=search_path), name="search")
        # self.app.mount("/assets/javascripts/workers", StaticFiles(directory=worker_path), name="workers")
        # self.app.mount("/assets/javascripts", StaticFiles(directory=javascripts_path), name="workers")

    def build_docs(self):
        """
        Build the documentation with mkdocs.
        """
        cwd = Path(os.getcwd())
        os.chdir(ModelDir.DOCS)
        subprocess.run("mkdocs build", shell=True, check=True)
        os.chdir(cwd)
        (ModelDir.DOCS / "site" / "images").resolve().mkdir(exist_ok=True)

    def set_host(self, host: str):
        """
        Set the IP address of the host.
        :param host: e.g. 127.0.0.1
        """
        self.host = str(host)

    def set_port(self, port: int):
        """
        Set the port.
        :param port: int, e.g. 5000
        """
        self.port = int(port)

    def run(self):
        """
        Running the application that is running the specified input project's run method.
        :return: None
        """
        if self.key_file_path and self.cert_file_path:
            uvicorn.run(
                self.app,
                host=self.host,
                port=self.port,
                log_level="info",
                ssl_keyfile=self.key_file_path,
                ssl_certfile=self.cert_file_path,
            )
        else:
            uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def __call__(self, *args, **kwargs):
        self.run()


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")
