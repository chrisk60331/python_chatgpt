import pytest
from unittest.mock import mock_open, patch
from typing import List, Tuple

from src.code_snippet import CodeSnippet, parse_code_snippets


class TestCodeSnippet:
    def test_init(self):
        snippet = "some code"
        code_snippet = CodeSnippet(snippet)
        assert code_snippet.snippet == snippet.strip()

        tuple_snippet = ("some", "code")
        code_snippet = CodeSnippet(tuple_snippet)
        assert code_snippet.snippet == "".join(tuple_snippet).strip()

    def test_save(self):
        snippet = "some code"
        extension = "py"
        file_name = "test"
        code_snippet = CodeSnippet(snippet)
        code_snippet.file_name = file_name
        with patch("builtins.open", mock_open()) as mock_file:
            code_snippet.save()
            mock_file.assert_called_once_with(f"{file_name}.{extension}", "w")
            mock_file.return_value.write.assert_called_once_with(snippet.strip())

    @pytest.mark.parametrize(
        "test_input,expected_output",
        [
            (
                "```python\nprint('hello, world')\n```",
                [("print('hello, world')", "py")],
            ),
            ("```sql\nSELECT * FROM table\n```", [("* FROM table", "sql")]),
            (
                "```java\npublic class HelloWorld {}\n```",
                [("public class HelloWorld {}", "jav")],
            ),
            (
                "```sh\necho 'hello, world'\n```",
                [("echo 'hello, world'", "sh")],
            ),
            ("```bash\nls -l\n```", [("ls -l", "sh")]),
        ],
    )
    def test_parse_code_snippets(
        self, test_input: str, expected_output: List[Tuple[CodeSnippet, str]]
    ):
        assert parse_code_snippets(test_input) == expected_output
