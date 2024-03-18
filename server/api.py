from flask import Flask
from flask_restx import Resource, Api, fields

import sys

sys.path.append("..")

from chat.simple_chat import run_llm

app = Flask(__name__)
api = Api(
    app,
    version="1.0.0",
    title="Chat API",
    doc="/swagger/",
)


@api.route("/")
class Index(Resource):
    def get(self):
        return {"title": api.title, "doc": api.doc, "api_version": api.version}


chat_ns = api.namespace("chat", description="Chat operations")
chat_input_model = api.model(
    "ChatInput",
    {
        "question": fields.String(required=True, description="The chat question"),
        "history": fields.List(
            fields.String, required=False, description="The chat history"
        ),
    },
)

chat_output_model = api.model(
    "ChatOutput",
    {
        "answer": fields.String(required=True, description="The chat answer"),
        "history": fields.List(
            fields.String, required=False, description="The chat history"
        ),
    },
)


@chat_ns.route("/")
class Chat(Resource):
    @chat_ns.expect(chat_input_model)
    @api.response(200, "Success", chat_output_model)
    def post(self):
        answer, history = run_llm(api.payload["question"], api.payload["history"])
        return {"answer": answer, "history": history}


if __name__ == "__main__":
    app.run(debug=True)
