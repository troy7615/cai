import openai
import gradio as gr

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "you are a 32 year old man who just had his house burn down and hate the world"},
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

# Use gr.Textbox directly for inputs and outputs
inputs = gr.Textbox(lines=7, label="Chat with AI")
outputs = gr.Textbox(label="Reply")

gr.Interface(
    fn=chatbot,
    inputs=inputs,
    outputs=outputs,
    title="AI Chatbot",
    description="Ask anything you want",
    theme="compact"
).launch(share=True)
