import logging
import openai
import streamlit
from dotenv import load_dotenv
from tools import assistant_tools
from assistant_manager import AssistantManager


def read_instructions(file_path):
    try:
        with open(file_path, encoding = "utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File {file_path} not found. Assistant instructions not available.")
        raise

def main():
    load_dotenv()
    logging.basicConfig(filename='app.log')

    client = openai.OpenAI()
    model = "gpt-3.5-turbo"

    streamlit.title("ðŸ“° Zpravodaj ðŸ“°")

    with streamlit.form(key="user_input_form"):
        topic_name = streamlit.text_input("VloÅ¾te tÃ©ma, na kterÃ© chcete dostat shrnutÃ­ aktuÃ¡lnÃ­ch novinek v ÄeÅ¡tinÄ›:")
        submit_button = streamlit.form_submit_button(label="Spustit")

        if submit_button:

            if "assistant" not in streamlit.session_state:
                assistant = client.beta.assistants.create(name="Zpravodaj",
                    model=model,
                    instructions=read_instructions("assistant_instructions.txt"),
                    tools=assistant_tools)
                streamlit.session_state["assistant"] = assistant

            if "thread" not in streamlit.session_state:                        
                thread = client.beta.threads.create()
                streamlit.session_state["thread"] = thread

            manager = AssistantManager(client, streamlit.session_state["assistant"], streamlit.session_state["thread"])

            manager.add_message_to_thread(role="user", content= f"UdÄ›lej shrnutÃ­ novinek na tÃ©ma {topic_name}")
            manager.run_assistant()
            manager.wait_for_run_to_complete()

            streamlit.write(manager.get_summary())

if __name__ == "__main__":
    main()