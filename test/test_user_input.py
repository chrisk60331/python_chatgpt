from unittest.mock import patch

from src.user_input import UserInput


class TestUserInput:
    @patch("builtins.input", side_effect=["line 1", "line 2", "done"])
    def test_multiline_input(self, mock_input):
        expected_output = "line 1line 2"
        assert UserInput.multiline_input() == expected_output
        mock_input.assert_called_with()
        assert mock_input.call_count == 3
