import gradio

from src.data.api_manager import CMR_ENDPOINTS

# from python_utils.ui.SeabornCharts import DataVisualizer # NOTE: This is here for reference later when it's time to work on visualizations.


def create_agent_interface_tab(agent_query_function) -> gradio.Tab:
    with gradio.Tab("Agent Interface") as _agent_interface_tab:
        with gradio.Row():
            agent_output = gradio.Textbox(label="Agent Output")
        with gradio.Row():
            user_query_text = gradio.Textbox(
                label="User Query", lines=5, placeholder="Enter LLM query here..."
            )
            query_submit_button = gradio.Button("Submit", variant="primary")
        query_submit_button.click(
            agent_query_function, inputs=user_query_text, outputs=agent_output
        )
    return _agent_interface_tab


def create_api_requester_tab(api_request_function) -> gradio.Tab:
    def update_api_parameters(cmr_endpoint):
        if cmr_endpoint in ["autocomplete", "collections"]:
            return (
                gradio.update(visible=True),
                gradio.update(visible=True),
                gradio.update(visible=True),
            )
        else:
            return (
                gradio.update(visible=True),
                gradio.update(visible=True),
                gradio.update(visible=False),
            )

    with gradio.Tab("API Requester") as _api_requester_tab:
        with gradio.Row():
            cmr_endpoint = gradio.Radio(
                choices=list(
                    zip(
                        [
                            endpoint.value for endpoint in CMR_ENDPOINTS
                        ],  # This is the frontend value
                        [
                            endpoint.name for endpoint in CMR_ENDPOINTS
                        ],  # This is the value passed to the change function
                    )
                ),
            )
        with gradio.Row():
            search_query = gradio.Textbox(
                value="MOIDS",
                label="Search Query",
                lines=1,
                placeholder="Enter search query here...",
            )
            page_size_parameter = gradio.Number(
                value=10, label="Page Size", visible=False
            )
            page_number_parameter = gradio.Number(
                value=1, label="Page Number", visible=False
            )
            offset_parameter = gradio.Number(value=0, label="Offset", visible=False)
        with gradio.Row():
            api_request_submit_button = gradio.Button(
                "Submit API Request", variant="primary"
            )
        with gradio.Row():
            api_request_output = gradio.TextArea(label="API Request Output")

        cmr_endpoint.change(
            update_api_parameters,
            inputs=cmr_endpoint,
            outputs=[page_size_parameter, page_number_parameter, offset_parameter],
        )

        api_request_submit_button.click(
            api_request_function,
            inputs=[
                cmr_endpoint,
                search_query,
                page_size_parameter,
                page_number_parameter,
                offset_parameter,
            ],
            outputs=api_request_output,
        )
    return _api_requester_tab


def create_data_visualization_tab() -> gradio.Tab:
    with gradio.Tab("Data Visualization") as _data_visualization_tab, gradio.Row():
        data_visualization = gradio.Textbox(label="Data Visualization")
    return _data_visualization_tab


def create_user_interface(agent_query_function, api_request_function) -> gradio.Blocks:
    with gradio.Blocks() as _interface:
        gradio.Markdown(value="# NASA CMR AI Agent Application")

        create_agent_interface_tab(agent_query_function)
        create_data_visualization_tab()
        create_api_requester_tab(api_request_function)

    return _interface
