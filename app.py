import openai
import gradio as gr
import os

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]

def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

# Gradio interface setup
inputs = gr.Textbox(lines=7, label="Chat with AI")
outputs = gr.Textbox(label="Reply")

gr.Interface(
    fn=chatbot,
    inputs=inputs,
    outputs=outputs,
    title="AI Chatbot",
    description="Ask anything you want"
).launch(server_name="0.0.0.0", server_port=8080)
