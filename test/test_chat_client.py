from unittest.mock import patch, Mock, call, mock_open

from src.chat_client import ChatClient


class TestChatClient:
    @patch("src.user_input.UserInput.multiline_input")
    def test_start(self, mock_input):
        chat_thread = Mock()
        client = ChatClient(chat_thread)
        mock_input.side_effect = ["hello", "/exit"]
        client.start()
        assert mock_input.call_count == 2
        assert chat_thread.send_message.call_count == 1

    @patch("builtins.print")
    def test_print_history(self, mock_print):
        chat_thread = Mock()
        chat_thread.history = ["message 1", "message 2", "message 3"]
        client = ChatClient(chat_thread)
        with patch("src.user_input.UserInput.multiline_input") as mock_input:
            mock_input.side_effect = ["/history", "/exit"]
            client.start()
        assert mock_input.call_count == 2
        expected_calls = [
            call("Conversation history:"),
            call("message 1"),
            call("message 2"),
            call("message 3"),
        ]
        assert all(
            _call in mock_print.mock_calls for _call in expected_calls
        ), mock_print.mock_calls

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='["message 1", "message 2", "message 3"]',
    )
    @patch("builtins.print")
    def test_import_history(
        self,
        mock_print,
        _mock_open,
    ):
        mock_open_expected_call_args = ["conversation.json", "r"]
        mock_print_expected_calls = [
            call("Conversation history:"),
            call("message 1"),
            call("message 2"),
            call("message 3"),
        ]
        chat_thread = Mock()
        chat_thread.history = ["message 1", "message 2", "message 3"]
        client = ChatClient(chat_thread)
        with patch("src.user_input.UserInput.multiline_input") as mock_input:
            mock_input.side_effect = ["/import", "/history", "/exit"]
            client.start()

        assert mock_input.call_count == 3
        _mock_open.assert_called_with(*mock_open_expected_call_args)
        assert all(
            _call in mock_print.mock_calls for _call in mock_print_expected_calls
        ), mock_print.mock_calls

    @patch("builtins.open")
    def test_export_history(self, _mock_open):
        expected_calls = [
            call("conversation.json", "w"),
            call().__enter__().write('["message 1", "message 2", "message 3"]'),
        ]

        chat_thread = Mock()
        chat_thread.history = ["message 1", "message 2", "message 3"]
        client = ChatClient(chat_thread)
        with patch("src.user_input.UserInput.multiline_input") as mock_input:
            mock_input.side_effect = ["/export", "/exit"]
            client.start()

        assert mock_input.call_count == 2
        assert all(
            _call in _mock_open.mock_calls for _call in expected_calls
        ), _mock_open.mock_calls
