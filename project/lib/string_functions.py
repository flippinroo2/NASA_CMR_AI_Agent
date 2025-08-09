def replace_double_newline(llm_output: str) -> str:
    return_string = llm_output.replace("\\n", "\n")
    return return_string.strip()
