from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("OPENAI_API_KEY")
print(f"API Key found: {api_key is not None}")
print(f"API Key starts with: {api_key[:8] if api_key else 'MISSING'}")

client = openai.OpenAI(api_key=api_key)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    python_code = data.get("code", "")

    if not python_code:
        return jsonify({"error": "No code provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"""Convert the following Python code to equivalent C++ code.
Return ONLY the C++ code with no explanation, no markdown, no backticks. Just the raw C++ code.

Python code:
{python_code}"""
            }]
        )
        cpp_code = response.choices[0].message.content
        return jsonify({"result": cpp_code})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
