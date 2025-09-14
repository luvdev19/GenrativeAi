import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__, static_folder="static")

# Set Gemini API key


# Load model once (fast response)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/prompt", methods=["POST"])
def prompt():
    data = request.get_json(silent=True) or {}
    prompt_text = data.get("prompt") or request.form.get("prompt")

    if not prompt_text:
        return jsonify({"error": "Missing 'prompt'"}), 400

    try:
        resp = model.generate_content(prompt_text)
        assistant_text = resp.text.strip()
        return jsonify({"response": assistant_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
