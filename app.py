import time
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv



# Use Flask to create a web server for the HTML template to access the chatbot


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
Assistant_ID = os.getenv('Assistant_ID')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire Flask app
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get("message", "")
    assistant_id = Assistant_ID
    # Use the new Responses API to get the assistant's reply
    response = client.chat.completions.create(
        model="gpt-4",  # or your preferred model
        messages=[{"role": "user", "content": user_message}],
        temperature=0.7
    )
    latest_message = response.choices[0].message.content if response.choices else "No response available"
    
    return jsonify({"response": latest_message})

@app.route('/chatbot')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

