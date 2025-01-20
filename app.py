import openai
import gradio as gr
import os
from flask import Flask, request, redirect, url_for

# Initialize Flask
app = Flask(__name__)

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Password to access the site
PASSWORD = os.getenv("ACCESS_PASSWORD", "yourpassword")  # You can set this in Render's environment variables

# Gradio app function
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

# Route for password protection
@app.route('/')
def home():
    password = request.args.get("password")
    print(f"Received password: {password}")  # Log the received password for debugging

    if password == PASSWORD:
        print("Password correct, launching Gradio interface...")  # Log when password is correct
        return gr.Interface(
            fn=chatbot,
            inputs=inputs,
            outputs=outputs,
            title="AI Chatbot",
            description="Ask anything you want"
        ).launch(inline=True, share=True)
    else:
        print("Password incorrect, prompting user...")  # Log when password is incorrect
        return '''
            <form method="get">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <input type="submit" value="Submit">
            </form>
        '''

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)
