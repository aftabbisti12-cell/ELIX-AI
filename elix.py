from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)  # Allows your HTML file to talk to this server

# The API key is pulled securely from Render's Environment Variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are ELIX, a helpful chemistry AI guide for new employees. 
Only answer chemistry, lab safety, and equipment questions. 
Keep answers short, professional, and friendly.
"""

@app.route('/')
def serve_home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)
    
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message.strip():
        return jsonify({"reply": "Please ask me something about chemistry."})
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="openai/gpt-oss-120b",
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Sorry, I had trouble thinking. Please try again."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)