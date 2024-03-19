import gradio as gr
from urllib.parse import urljoin
import requests

api_base_url = "http://127.0.0.1:5000/"
bot_status = ""


def respond(message, chat_history):
    global bot_status
    url = urljoin(api_base_url, "chat")
    payload = {"question": message, "status": bot_status}
    response = requests.post(url, json=payload)
    response_json = response.json()
    bot_message = response_json["answer"]
    bot_status = response_json["status"]
    # import pdb; pdb.set_trace()
    chat_history.append(
        tuple((message, bot_message))
    )  # Be sure to have a tuple, otherwise we get a list and an exception
    return "", chat_history


with gr.Blocks() as demo:
    with gr.Row():                
        toggle_dark = gr.Button(value="Toggle Dark", size="sm", scale=2)
        toggle_dark.click( None,
        js="""
        () => {
            document.body.classList.toggle('dark');
        }
        """,
    )

    with gr.Row():
        chatbot = gr.Chatbot()
    with gr.Row():
        msg = gr.Textbox(scale=4, label="Prompt")
        btn = gr.Button("Submit")
        clear = gr.ClearButton(components=[msg, chatbot], value="Clear console")

    btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()
