def sanitize_llm_output(llm_output: str) -> str:
    _return_string = llm_output.replace("\\n", "\n")
    return _return_string.strip()
