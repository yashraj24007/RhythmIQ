#!/usr/bin/env python3
"""
Minimal Python API for RhythmIQ
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import cv2
import numpy as np
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables
model = None
class_names = ['F', 'M', 'N', 'Q', 'S', 'V']

def load_model():
    """Load the trained model"""
    global model
    try:
        model_path = "05_trained_models/rythmguard_model.joblib"
        logger.info(f"Loading model from {model_path}")
        
        loaded_data = joblib.load(model_path)
        if isinstance(loaded_data, dict) and 'model' in loaded_data:
            model = loaded_data['model']  # Extract actual model
        else:
            model = loaded_data
            
        logger.info("✅ Model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        return False

def preprocess_image(image_path):
    """Preprocess image to match training format"""
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return None
            
        # Resize to training dimensions (224x224)
        image_resized = cv2.resize(image, (224, 224))
        
        # Convert BGR to RGB (match training preprocessing)
        image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        image_normalized = image_rgb.astype(np.float32) / 255.0
        
        # Flatten (224 * 224 * 3 = 150,528 features)
        image_flattened = image_normalized.flatten()
        
        logger.info(f"Image preprocessed: shape {image_flattened.shape}")
        return image_flattened.reshape(1, -1)
        
    except Exception as e:
        logger.error(f"Preprocessing error: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes': class_names
    })

@app.route('/analyze', methods=['POST'])
def analyze_ecg():
    """Analyze uploaded ECG image"""
    try:
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        logger.info(f"Analyzing file: {file.filename}")
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Preprocess image
            processed_image = preprocess_image(temp_path)
            if processed_image is None:
                return jsonify({'error': 'Image preprocessing failed'}), 400
            
            # Make prediction
            prediction_idx = model.predict(processed_image)[0]
            probabilities = model.predict_proba(processed_image)[0]
            confidence = float(np.max(probabilities))
            
            # Map prediction index to class name
            predicted_class = class_names[prediction_idx] if prediction_idx < len(class_names) else str(prediction_idx)
            
            result = {
                'success': True,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.1f}%",
                'filename': file.filename
            }
            
            logger.info(f"Prediction: {predicted_class} (confidence: {confidence:.3f})")
            return jsonify(result)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("🫀 Starting RhythmIQ Minimal API...")
    
    # Load model
    if not load_model():
        print("❌ Failed to load model. Exiting.")
        exit(1)
    
    print("✅ Model loaded successfully")
    print("🚀 Starting server on http://localhost:8083")
    app.run(host='0.0.0.0', port=8083, debug=False)