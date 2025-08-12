from gradio import (
    Blocks,
    Button,
    Markdown,
    Row,
    Tab,
    Textbox,
)


def create_agent_interface_tab(agent_query_function) -> Tab:
    """
    Creates a tab within the gradio app for interacting with the agentic application.

    Args:
        agent_query_function (function): The function to be called when the user submits a query to the agentic application.

    Returns:
        Tab: The agent interface tab.
    """
    with Tab("Agent Interface") as agent_interface_tab:
        with Row():
            agent_output = Textbox(label="Agent Output")
        with Row():
            user_query_text = Textbox(
                label="User Query", lines=5, placeholder="Enter LLM query here..."
            )
            query_submit_button = Button("Submit", variant="primary")
        query_submit_button.click(
            agent_query_function, inputs=user_query_text, outputs=agent_output
        )
    return agent_interface_tab


def create_data_visualization_tab() -> Tab:
    """
    Creates a tab within the gradio app for visualizing data based on the output from the application.

    Returns:
        Tab: The data visualization tab.
    """
    with Tab("Data Visualization") as data_visualization_tab, Row():
        data_visualization = Textbox(label="Data Visualization")
    return data_visualization_tab


def create_user_interface(agent_query_function) -> Blocks:
    """
    Creates the entire gradio interface by calling sub-functions for each individual tab.

    Args:
        agent_query_function (function): The function to be called when the user submits a query to the agentic application.

    Returns:
        Blocks: The gradio interface with the agent and data visualization tabs.
    """
    with Blocks() as _interface:
        Markdown(value="# NASA CMR AI Agent Application")

        create_agent_interface_tab(agent_query_function)
        create_data_visualization_tab()

    return _interface
