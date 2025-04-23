from flask import Flask, request, render_template, jsonify
import os
from core import run_agent
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_query():
    """Process the user query using the agent"""
    # Check if image is in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    # Get the uploaded file
    image_file = request.files['image']
    question = request.form.get('question', '')
    
    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save the uploaded image
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)
    
    # Run the agent
    try:
        result = run_agent(image_path, question)
        
        # Get tool outputs
        tool_outputs = result.get('tool_outputs', {})
        extracted_text = tool_outputs.get('text_extraction', "No text extracted")
        building_code = tool_outputs.get('building_code_retriever', "No building code retrieved")
        
        # Get final answer
        answer = result.get('result', "No answer generated")
        
        return jsonify({
            'answer': answer,
            'extractedText': extracted_text,
            'buildingCode': building_code
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary file
        if os.path.exists(image_path):
            os.remove(image_path)

@app.route('/samples/<sample>')
def serve_sample(sample):
    """Serve sample images"""
    return app.send_static_file(f'samples/{sample}')

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True)
