import logging
import re

logging.basicConfig(level=logging.INFO)


class CodeSnippet:
    def __init__(self, snippet: str):
        if isinstance(snippet, tuple):
            snippet = "".join(snippet)
        self.snippet = snippet.strip()
        self.file_name = None

    def save(self):
        logging.info(f"saving {self.file_name}")
        with open(self.file_name, "w") as snippet_file:
            snippet_file.write(self.snippet)

    def __str__(self):
        return self.snippet


def parse_code_snippets(message):
    patterns = {
        "py": r"```\s?python\n([\s\S]*?)```",
        "sql": r"```\s?sql\n([\s\S]*?)```",
        "jav": r"```\s?java\n([\s\S]*?)```",
        "sh": r"```\s?((ba|z|k|f)?sh)?\n([\s\S]*?)```",
    }
    return [
        CodeSnippet(snippet)
        for extension, pattern in patterns.items()
        for snippet in re.findall(pattern, message, re.IGNORECASE)
    ]
