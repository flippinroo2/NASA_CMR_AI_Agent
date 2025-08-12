import gradio


def create_agent_interface_tab(agent_query_function) -> gradio.Tab:
    """
    Creates a tab within the gradio app for interacting with the agentic application.

    Args:
        agent_query_function (function): The function to be called when the user submits a query to the agentic application.

    Returns:
        gradio.Tab: The agent interface tab.
    """
    with gradio.Tab("Agent Interface") as agent_interface_tab:
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
    return agent_interface_tab


def create_data_visualization_tab() -> gradio.Tab:
    """
    Creates a tab within the gradio app for visualizing data based on the output from the application.

    Returns:
        gradio.Tab: The data visualization tab.
    """
    with gradio.Tab("Data Visualization") as data_visualization_tab, gradio.Row():
        data_visualization = gradio.Textbox(label="Data Visualization")
    return data_visualization_tab


def create_user_interface(agent_query_function) -> gradio.Blocks:
    """
    Creates the entire gradio interface by calling sub-functions for each individual tab.

    Args:
        agent_query_function (function): The function to be called when the user submits a query to the agentic application.

    Returns:
        gradio.Blocks: The gradio interface with the agent and data visualization tabs.
    """
    with gradio.Blocks() as _interface:
        gradio.Markdown(value="# NASA CMR AI Agent Application")

        create_agent_interface_tab(agent_query_function)
        create_data_visualization_tab()

    return _interface
