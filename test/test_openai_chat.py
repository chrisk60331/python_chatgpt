from unittest import mock

import openai

from src.openai_chat import OpenAIChat

ENGINES = ("gpt-3.5-turbo",)


class MockResponse:
    def __init__(self, message):
        self.choices = [{"message": message}]


class TestOpenAIChat:
    @mock.patch.object(openai, "api_key", "test-api-key")
    def test_get_response(self):
        chat = OpenAIChat(api_key="test-api-key")
        messages = [{"role": "user", "content": "Hi!"}]
        expected_responses = [("gpt-3.5-turbo", "Hello! How can I assist you?")]
        with mock.patch.object(chat.api_client.ChatCompletion, "create") as mock_chat:
            mock_chat.return_value = MockResponse(expected_responses[0][1])
            responses = chat.get_response(messages=messages)
            assert responses == expected_responses

    def test_label_code(self):
        chat = OpenAIChat(api_key="test-api-key")
        code_snippet = 'print("Hello, world!")'
        expected_label = "print_hello_world"
        with mock.patch.object(chat, "get_response") as mock_get_response:
            mock_get_response.return_value = [
                ("gpt-3.5-turbo", {"content": f"{expected_label}"}),
            ]
            label = chat.label_code(code_snippet)
            assert label == expected_label
