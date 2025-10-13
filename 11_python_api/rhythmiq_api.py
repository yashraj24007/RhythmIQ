#!/usr/bin/env python3
"""
🫀 RhythmIQ Python ML API
========================
Lightweight Flask API serving the trained ECG classification model.
"""

import os
import sys
import joblib
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import io

# Add paths for custom modules
sys.path.append('../02_preprocessing')

try:
    from ecg_preprocessor import ECGPreprocessor
    from severity_predictor import SeverityPredictor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

app = Flask(__name__)

# Global variables
model = None
class_names = None
preprocessor = None
severity_predictor = None

def load_model():
    """Load the trained ECG model"""
    global model, class_names, preprocessor, severity_predictor
    
    try:
        # Load model
        model_path = '../05_trained_models/rythmguard_model.joblib'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        print("📁 Loading trained model...")
        model_data = joblib.load(model_path)
        
        if isinstance(model_data, dict):
            model = model_data['model']
            class_names = model_data['class_names']
        else:
            model = model_data
            class_names = ['F', 'M', 'N', 'Q', 'S', 'V']
        
        # Initialize preprocessor and severity predictor
        preprocessor = ECGPreprocessor('../01_data', target_size=(224, 224))
        severity_predictor = SeverityPredictor()
        
        print(f"✅ Model loaded successfully!")
        print(f"🎯 Classes: {class_names}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'RhythmIQ ML API',
        'model_loaded': model is not None
    })

@app.route('/analyze', methods=['POST'])
def analyze_ecg():
    """Analyze ECG image"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({'success': False, 'error': 'Model not loaded'}), 500
        
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Process image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Preprocess image
        processed_img = preprocessor.preprocess_image(np.array(image))
        if processed_img is None:
            return jsonify({'success': False, 'error': 'Failed to process image'}), 400
        
        # Make prediction
        flattened = processed_img.flatten().reshape(1, -1)
        prediction = model.predict(flattened)[0]
        probabilities = model.predict_proba(flattened)[0]
        
        predicted_class = class_names[prediction]
        confidence = float(max(probabilities))
        
        # Get severity prediction
        severity_result = severity_predictor.predict_severity_rule_based(predicted_class)
        
        result = {
            'success': True,
            'predicted_class': predicted_class,
            'confidence': confidence,
            'confidence_percentage': f"{confidence*100:.1f}%",
            'severity': severity_result['severity'],
            'severity_confidence': severity_result['confidence'],
            'filename': file.filename
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🫀 RhythmIQ Python ML API Starting...")
    print("=" * 50)
    
    # Load model at startup
    if not load_model():
        print("❌ Failed to start API - model loading failed")
        sys.exit(1)
    
    print("🚀 Starting Flask server on port 8083...")
    app.run(host='0.0.0.0', port=8083, debug=False)