# Friday AI Assistant

A simple AI assistant named `Friday` built as a Python CLI project.

## Features

- CLI chat loop
- Optional OpenAI integration when `OPENAI_API_KEY` is set
- Basic local fallback commands when no API key is available

## Setup

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Optionally set your OpenAI API key. You can either:

- Use environment variables:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

- Or edit the `.env` file that was created:

```bash
# Edit .env and replace 'your_api_key_here' with your actual OpenAI API key
```

To get your OpenAI API key:
1. Go to https://platform.openai.com/account/api-keys
2. Create a new API key
3. Copy and paste it into `.env` as `OPENAI_API_KEY=sk-...`

### Test OpenAI Connection

After setting your API key, test the connection:

```bash
python test_openai.py
```

This will verify Friday can communicate with OpenAI API before running the full server.

Then edit `.env` and set your key. Restart your terminal or use `set` for the current session if using env vars.

## Run

```bash
python friday.py
```

### Web UI

```bash
python server.py
```

Open `http://127.0.0.1:5000` in your browser to use the Friday interface.

## Usage

- Type a question or request and press Enter.
- Use `help` to see available commands.
- Use `exit` or `quit` to close Friday.
- Friday will address you as Boss in conversation.
- In the web UI, click the microphone button to speak your query.
- Use the TTS toggle to enable or disable Friday speaking responses.
- Friday uses one fixed integrated voice for all spoken responses.
