import logging
import openai
from dotenv import load_dotenv
from tools import assistant_tools
from assistant_manager import AssistantManager

load_dotenv()
logging.basicConfig(filename='app.log')

client = openai.OpenAI()
model = "gpt-3.5-turbo"

def read_instructions(file_path):
    try:
        with open(file_path, encoding = "utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File {file_path} not found. Assistant instructions not available.")
        raise

assistant = client.beta.assistants.create(name="Zpravodaj",
    model=model,
    instructions=read_instructions("assistant_instructions.txt"),
    tools=assistant_tools)
thread = client.beta.threads.create()

manager = AssistantManager(client, assistant, thread)
print(manager.assistant.id)

topic = "chci zpravy na tema bicoin"
manager.add_message_to_thread(role="user", content= f"Udělej shrnutí novinek na téma {topic}")
manager.run_assistant()
manager.wait_for_run_to_complete()
print(manager.get_summary())