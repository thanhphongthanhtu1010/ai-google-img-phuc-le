import os
import google.generativeai as genai
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for

bp = Blueprint('views', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = file.filename
            filepath = os.path.join('app/static', filename)
            file.save(filepath)
            
            # Configure Gemini API
            genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
            
            try:
                uploaded_file = genai.upload_file(filepath, mime_type="image/jpeg")
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash-latest",
                    generation_config={
                        "temperature": 1,
                        "top_p": 0.95,
                        "top_k": 64,
                        "max_output_tokens": 8192,
                        "response_mime_type": "text/plain",
                    },
                )
                chat_session = model.start_chat(
                    history=[
                        {
                            "role": "user",
                            "parts": [
                                "Mô tả bức ảnh này",
                                uploaded_file,
                            ],
                        },
                    ]
                )
                response = chat_session.send_message("Mô tả bức ảnh này")
                return render_template('index.html', response=response.text, filename=filename)
            except Exception as e:
                flash(f'An error occurred: {e}')
                return redirect(request.url)
    
    return render_template('index.html')
