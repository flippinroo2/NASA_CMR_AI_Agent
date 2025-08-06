import gradio
import uvicorn
from fastapi import FastAPI

from config import Configuration
from src.data.api_manager import CMR_ENDPOINTS, APIManager, CMRQueryParameters
from src.user_interface.gui import create_user_interface

print("\n__init__.py\n")  # TODO: Remove print statement here

app = FastAPI()

# TODO: DECIDE IF THIS IS THE ROUTE TO GO, OR IF IT SHOULD JUST ALL BE HANDLED IN __main__.py???
# NOTE: This is left in here for me to use with my debugger


def query_agents(*args, **kwargs):
    data = APIManager.query_cmr(CMR_ENDPOINTS.AUTOCOMPLETE, params={"q": "MODIS"})
    return data


user_interface: gradio.Blocks = create_user_interface(query_agents)
app = gradio.mount_gradio_app(app, user_interface, path="")

if __name__ == "__main__":
    config = Configuration()
    uvicorn.run(app, host=config.host, port=config.port)
