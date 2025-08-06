from config import Configuration
import uvicorn
from src.data.api_manager import APIManager, CMR_ENDPOINTS, CMRQueryParameters
from src.user_interface.gui import create_user_interface
from fastapi import FastAPI
import gradio

print("\n__init__.py\n")

app = FastAPI() # This is used to enable concurrent handling of requests. We mount the gradio interface as a FastAPI endpoint and then ...???

# TODO: DECIDE IF THIS IS THE ROUTE TO GO, OR IF IT SHOULD JUST ALL BE HANDLED IN __main__.py???

def query_agents(*args, **kwargs):
    data = APIManager.query_cmr(CMR_ENDPOINTS.AUTOCOMPLETE, params={"q": "MODIS"})
    return data

user_interface: gradio.Blocks = create_user_interface(query_agents)
app = gradio.mount_gradio_app(app, user_interface, path="")

if __name__ == "__main__":
    config = Configuration()
    uvicorn.run(app, host=config.host, port=config.port)