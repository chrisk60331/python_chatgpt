# Python ChatGPT

Python ChatGPT is a Python module that allows you to have threaded conversations with OpenAI's GPT-3 language model from the command line.

You will need an API key from openAI. To get one, sign up at [open ai](https://platform.openai.com/account/api-keys) and spit out an api key.

## Installation

1. Clone the repository:

```
git clone https://github.com/chrisk60331/python_chatgpt.git
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=<your-api-key>
```

## Usage

Run the program:
```python 
python src/main.py
```

## Testing

ChatGPT is tested using pytest. To run the tests, simply run the following command:

```bash
pytest .
```
