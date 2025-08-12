from src.llm.workflow.workflow_manager import WorkflowManager


def test_01(get_fixture_workflow_manager: WorkflowManager) -> None:
    if get_fixture_workflow_manager.state_graph is not None:
        # compiled_state_graph: CompiledStateGraph = (
        #     get_fixture_workflow_manager.state_graph.compile()
        # )
        print("TODO: Write unit test here")
