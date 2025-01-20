import openai
import gradio as gr
import os
from flask import Flask, request, redirect, url_for
import socket

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Password for access
PASSWORD = os.getenv("ACCESS_PASSWORD", "yourpassword")  # Set this in Render's environment variables

# Gradio chatbot function
messages = [{"role": "system", "content": "You are a helpful and kind AI Assistant."}]

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
    
    if password == PASSWORD:
        # If password is correct, start Gradio interface
        interface = gr.Interface(
            fn=chatbot,
            inputs=inputs,
            outputs=outputs,
            title="AI Chatbot",
            description="Ask anything you want"
        )
        interface.launch(share=True, inline=True, server_port=int(os.getenv("PORT", 8080)))  # Use Render's port here
        return redirect("/gradio")  # Redirect to Gradio interface if valid password
    else:
        # If password is incorrect, show the password prompt
        return '''
            <form method="get">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <input type="submit" value="Submit">
            </form>
        '''

# Start Flask app on the dynamic port provided by Render
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))  # Use Render's provided dynamic port
    app.run(debug=False, host="0.0.0.0", port=port)
