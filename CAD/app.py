from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from cad_processor import CADProcessor
from cost_calculator import CostCalculator
from pdf_generator import PDFGenerator
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
cad_processor = CADProcessor()
cost_calculator = CostCalculator()
pdf_generator = PDFGenerator()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'dxf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process CAD file
            geometry_data = cad_processor.process_dxf(filepath)
            
            # Get material and thickness from form
            material = request.form.get('material', 'steel')
            thickness = float(request.form.get('thickness', 1.0))
            
            # Calculate costs
            cutting_length = geometry_data['total_length']
            machining_time = cost_calculator.calculate_machining_time(cutting_length, material, thickness)
            total_cost = cost_calculator.calculate_total_cost(machining_time, material, thickness, cutting_length)
            
            # Generate PDF
            pdf_path = pdf_generator.generate_quotation(
                geometry_data, material, thickness, machining_time, total_cost
            )
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'cutting_length': round(cutting_length, 2),
                'machining_time': round(machining_time, 2),
                'total_cost': round(total_cost, 2),
                'pdf_path': pdf_path
            })
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_pdf(filename):
    try:
        return send_file(
            os.path.join('temp_pdfs', filename),
            as_attachment=True,
            download_name=f'cnc_quotation_{filename}'
        )
    except FileNotFoundError:
        return jsonify({'error': 'PDF not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
