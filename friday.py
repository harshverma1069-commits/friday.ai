import os
import sys
import time

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    import openai
except ImportError:
    openai = None

PROJECT_NAME = "Friday"
USER_TITLE = "Boss"
PROMPT = "> "

if load_dotenv:
    load_dotenv()

LOCAL_COMMANDS = {
    "help": "Show this help text.",
    "exit": "Exit Friday.",
    "quit": "Exit Friday.",
    "time": "Show the current local time.",
    "about": "Show information about Friday.",
}


def print_help():
    print(f"{PROJECT_NAME} commands:")
    for command, description in LOCAL_COMMANDS.items():
        print(f"  {command:6} - {description}")


def get_openai_response(message: str, history: list = None) -> str:
    if not openai:
        return "OpenAI package is not installed. Install it with `pip install -r requirements.txt`."

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key and load_dotenv:
        load_dotenv()
        api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return "OPENAI_API_KEY is not set. Set it in your environment or add it to a .env file to use the AI assistant."

    try:
        messages = [
            {
                "role": "system",
                "content": "You are Friday, a helpful AI assistant. Always address the user as Boss, and call them Boss in every message.",
            }
        ]
        if history:
            for msg in history:
                role = "assistant" if msg["role"] == "bot" else "user"
                messages.append({"role": role, "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
    except AttributeError:
        messages = [
            {
                "role": "system",
                "content": "You are Friday, a helpful AI assistant. Always address the user as Boss, and call them Boss in every message.",
            }
        ]
        if history:
            for msg in history:
                role = "assistant" if msg["role"] == "bot" else "user"
                messages.append({"role": role, "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
    except Exception as exc:
        return f"OpenAI request failed: {exc}"

    try:
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"OpenAI response parsing failed: {exc}"


def get_friday_response(message: str, history: list = None) -> str:
    normalized = message.strip().lower()
    if normalized in LOCAL_COMMANDS:
        return local_fallback(message)

    if os.environ.get("OPENAI_API_KEY"):
        return get_openai_response(message, history)

    return local_fallback(message)


def local_fallback(message: str) -> str:
    normalized = message.strip().lower()
    if normalized in ("exit", "quit"):
        return "exit"
    if normalized == "help":
        print_help()
        return ""
    if normalized == "time":
        return f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, {USER_TITLE}."
    if normalized == "about":
        return f"{PROJECT_NAME} is a local AI assistant prototype, {USER_TITLE}. Set OPENAI_API_KEY to enable GPT-powered responses."
    return f"I can help with basic commands, {USER_TITLE}. Set OPENAI_API_KEY to enable full AI responses. Type `help` to see available commands."


def main():
    print(f"Welcome to {PROJECT_NAME}! Type `help` for commands.")
    if openai is None:
        print("Note: openai package is not installed. Install dependencies with `pip install -r requirements.txt`.")
    elif load_dotenv is None:
        print("Note: python-dotenv is not installed. Install dependencies with `pip install -r requirements.txt` to enable .env support.")

    while True:
        try:
            user_input = input(PROMPT).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        if user_input.lower() in LOCAL_COMMANDS:
            result = local_fallback(user_input)
            if result == "exit":
                print("Goodbye.")
                break
            if result:
                print(result)
            continue

        if openai and os.environ.get("OPENAI_API_KEY"):
            answer = get_openai_response(user_input)
            print(answer)
        else:
            print(local_fallback(user_input))


if __name__ == "__main__":
    main()
