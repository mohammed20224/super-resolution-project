from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from enhance import ImageEnhancer
import time

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize enhancer
enhancer = ImageEnhancer()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, BMP, WEBP'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        input_filename = f"{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)
        
        # Return success
        return jsonify({
            'success': True,
            'filename': input_filename,
            'message': 'File uploaded successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/enhance', methods=['POST'])
def enhance():
    """Enhance uploaded image"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        # Paths
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"enhanced_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Check if input file exists
        if not os.path.exists(input_path):
            return jsonify({'error': 'Input file not found'}), 404
        
        # Enhance image
        success = enhancer.enhance_image(input_path, output_path)
        
        if success:
            return jsonify({
                'success': True,
                'input_filename': filename,
                'output_filename': output_filename,
                'message': 'Image enhanced successfully!'
            })
        else:
            return jsonify({'error': 'Failed to enhance image'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    """Serve images"""
    try:
        if folder == 'uploads':
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif folder == 'outputs':
            return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))
        else:
            return jsonify({'error': 'Invalid folder'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 404


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting Super Resolution App")
    print("=" * 50)
    print("Loading AI model... This may take a moment...")
    
    # Pre-load model
    enhancer.load_model()
    
    print("\n✓ Server ready!")
    print("📌 Open your browser and go to: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
