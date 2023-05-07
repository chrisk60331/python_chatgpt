# OpenAI Chat

This is a Python module that lets you have threaded conversations with OpenAI's GPT-3 AI language model. You can run it from the command line.

## Installation

1. Clone this repository to your local machine:

```
git clone https://github.com/your-username/openai-chat.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:

```
export OPENAI_API_KEY="your_api_key"
```

## Usage

To start a conversation with OpenAI, run the following command:

```
python main.py
```

This will start a chat session in the command line. Type in your messages, and the AI will respond.

You can also run the unit tests by running the following command:

```
python -m unittest discover tests/
```

## Configuration

You can configure the behavior of the chat client by modifying the `config.py` file. Here are some of the available settings:

- `ENGINE`: The OpenAI engine to use for generating responses. Possible values are "davinci", "curie", and "babbage".
- `MAX_TOKENS`: The maximum number of tokens to generate for each response.
- `STOP`: A list of stop sequences to use for generating responses. The AI will stop generating text once it encounters one of these sequences.
- `RELEVANT_KEYWORDS`: A list of keywords to look for in the conversation history when generating responses. The AI will try to generate responses that are relevant to these keywords.

## Contributing

If you find a bug or have an idea for a new feature, please open an issue on this repository. Pull requests are also welcome!
