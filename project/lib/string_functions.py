def replace_double_newline(llm_output: str) -> str:
    _return_string = llm_output.replace("\\n", "\n")
    return _return_string.strip()
