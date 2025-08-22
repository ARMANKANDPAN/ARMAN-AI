
from flask import Flask, render_template, request, jsonify
import os
import requests
import io
import google.generativeai as genai


# Configure API keys
genai.configure(api_key=os.environ.get("GEMINI_API_KEY") or "AIzaSyAcBL9kGSt6ctz0YvMSECifsDvT4uhfmos")



app = Flask(__name__)

# Google Drive file ID for the background image
GOOGLE_DRIVE_FILE_ID = '1ras_8Ka9N_RGtTOHtbdsicH4OZw7rqOM'
BACKGROUND_IMAGE_PATH = os.path.join('static', 'background.jpg')

def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : file_id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : file_id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Download the background image when the app starts
if not os.path.exists(BACKGROUND_IMAGE_PATH):
    print(f"Downloading background image to {BACKGROUND_IMAGE_PATH}...")
    download_file_from_google_drive(GOOGLE_DRIVE_FILE_ID, BACKGROUND_IMAGE_PATH)
    print("Background image downloaded.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # In a real application, you would integrate your AI model here
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_message)
        text_response = response.text
        return jsonify({'text_response': text_response})
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'response': f'Sorry, there was an error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='0.0.0.0')