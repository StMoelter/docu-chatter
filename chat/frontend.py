import gradio as gr
import random
import time
from backend import run_llm

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Prompt")
    btn = gr.Button("Submit")
    clear = gr.ClearButton(components=[msg, chatbot], value="Clear console")

    def respond(message, chat_history):
        bot_message = run_llm(message, chat_history)
        chat_history.append(tuple((message, bot_message['answer']))) # Be sure to have a tuple, otherwise we get a list and an exception
        return "", chat_history
    
    btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()
