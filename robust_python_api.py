"""
Robust Python API for ECG Analysis - Fixed Version
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np
import cv2
from PIL import Image
import tempfile
from datetime import datetime
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class RobustECGAPI:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.class_names = ['F', 'M', 'N', 'Q', 'S', 'V']
        self.class_descriptions = {
            'N': 'Normal beat (sinus rhythm)',
            'S': 'Supraventricular beat (atrial premature)',
            'V': 'Ventricular beat (PVC - Premature Ventricular Contraction)',
            'F': 'Fusion beat (ventricular + normal)',
            'Q': 'Unknown/Paced beat',
            'M': 'Myocardial Infarction'
        }
        self.severity_mapping = {
            'N': ('Normal', 'Low'),
            'S': ('Moderate', 'Medium'),
            'V': ('Moderate', 'Medium'),
            'F': ('Severe', 'High'),
            'Q': ('Moderate', 'Medium'),
            'M': ('Critical', 'Very High')
        }
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model safely"""
        try:
            model_path = '05_trained_models/rythmguard_model.joblib'
            
            if not os.path.exists(model_path):
                logger.error(f"Model file not found: {model_path}")
                return False
            
            logger.info(f"Loading model from {model_path}")
            loaded_data = joblib.load(model_path)
            
            if isinstance(loaded_data, dict) and 'model' in loaded_data:
                self.model = loaded_data['model']
                if 'class_names' in loaded_data:
                    self.class_names = loaded_data['class_names']
                logger.info("✅ Model loaded from dictionary successfully")
            else:
                self.model = loaded_data
                logger.info("✅ Model loaded directly successfully")
            
            # Verify model has predict method
            if not hasattr(self.model, 'predict'):
                logger.error("❌ Loaded object doesn't have predict method")
                return False
            
            self.model_loaded = True
            logger.info(f"✅ Model ready with classes: {self.class_names}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            traceback.print_exc()
            return False
    
    def preprocess_image_safe(self, image_path):
        """Safely preprocess ECG image"""
        try:
            logger.info(f"Preprocessing image: {image_path}")
            
            # Load image with error handling
            image = None
            try:
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            except Exception as e:
                logger.warning(f"OpenCV failed to load image: {e}")
            
            if image is None:
                try:
                    pil_image = Image.open(image_path).convert('RGB')
                    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                    logger.info("Image loaded with PIL")
                except Exception as e:
                    logger.error(f"Failed to load image with PIL: {e}")
                    return None
            else:
                logger.info("Image loaded with OpenCV")
            
            # Resize image to match training dimensions
            target_size = (224, 224)
            image_resized = cv2.resize(image, target_size)
            
            # Convert BGR to RGB (to match training preprocessing)
            if len(image_resized.shape) == 3:
                image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
            else:
                # If grayscale, convert to RGB
                image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_GRAY2RGB)
            
            # Normalize pixel values to [0, 1] (as per training)
            image_normalized = image_rgb.astype(np.float32) / 255.0
            
            # Flatten for Random Forest model (224 * 224 * 3 = 150,528 features)
            image_flattened = image_normalized.flatten()
            
            logger.info(f"Image preprocessed successfully. Shape: {image_flattened.shape}")
            return image_flattened.reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Error in preprocessing: {e}")
            traceback.print_exc()
            return None
    
    def predict_safe(self, image_path):
        """Make prediction with comprehensive error handling"""
        try:
            if not self.model_loaded:
                return {
                    'success': False,
                    'error': 'Model not loaded',
                    'predicted_class': None,
                    'confidence': None,
                    'confidence_percentage': None,
                    'description': None,
                    'severity': None
                }
            
            # Preprocess image
            processed_image = self.preprocess_image_safe(image_path)
            if processed_image is None:
                return {
                    'success': False,
                    'error': 'Failed to preprocess image',
                    'predicted_class': None,
                    'confidence': None,
                    'confidence_percentage': None,
                    'description': None,
                    'severity': None
                }
            
            # Make prediction
            logger.info("Making prediction...")
            prediction = self.model.predict(processed_image)[0]
            probabilities = self.model.predict_proba(processed_image)[0]
            
            # Get predicted class
            if isinstance(prediction, (int, np.integer)):
                if 0 <= prediction < len(self.class_names):
                    predicted_class = self.class_names[prediction]
                else:
                    predicted_class = 'Unknown'
            else:
                predicted_class = str(prediction)
            
            # Get confidence
            confidence = float(np.max(probabilities))
            
            # Get severity
            severity_info = self.severity_mapping.get(predicted_class, ('Moderate', 'Medium'))
            
            result = {
                'success': True,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.1f}%",
                'description': self.class_descriptions.get(predicted_class, 'Unknown condition'),
                'severity': severity_info[0],
                'severity_level': severity_info[1],
                'timestamp': datetime.now().isoformat(),
                'model_info': {
                    'classes': self.class_names,
                    'total_classes': len(self.class_names)
                }
            }
            
            logger.info(f"Prediction successful: {predicted_class} ({confidence:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}',
                'predicted_class': None,
                'confidence': None,
                'confidence_percentage': None,
                'description': None,
                'severity': None
            }

# Initialize API
logger.info("Initializing RobustECGAPI...")
ecg_api = RobustECGAPI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'model_loaded': ecg_api.model_loaded,
            'classes': ecg_api.class_names,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0'
        })
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'error',
            'model_loaded': False,
            'error': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_ecg():
    """ECG analysis endpoint with robust error handling"""
    temp_path = None
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided',
                'predicted_class': None,
                'confidence': None,
                'confidence_percentage': None,
                'description': None,
                'severity': None
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected',
                'predicted_class': None,
                'confidence': None,
                'confidence_percentage': None,
                'description': None,
                'severity': None
            }), 400
        
        logger.info(f"Analyzing file: {file.filename}")
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
            logger.info(f"File saved to: {temp_path}")
        
        # Analyze
        result = ecg_api.predict_safe(temp_path)
        result['filename'] = file.filename
        
        # Clean up
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        
        if result['success']:
            logger.info(f"Analysis completed successfully for {file.filename}")
            return jsonify(result)
        else:
            logger.warning(f"Analysis failed for {file.filename}: {result.get('error')}")
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error in analyze_ecg: {e}")
        traceback.print_exc()
        
        # Clean up on error
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}',
            'predicted_class': None,
            'confidence': None,
            'confidence_percentage': None,
            'description': None,
            'severity': None
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        return jsonify({
            'model_loaded': ecg_api.model_loaded,
            'classes': ecg_api.class_names,
            'descriptions': ecg_api.class_descriptions,
            'severity_mapping': ecg_api.severity_mapping,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in model_info: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🫀 RhythmIQ Robust Python API v2.0")
    print("=" * 50)
    
    if not ecg_api.model_loaded:
        print("❌ Failed to load model - exiting")
        exit(1)
    
    print("✅ All models loaded successfully!")
    print("🚀 Starting robust API server on http://localhost:8083")
    print("🔗 Ready for Java web app integration")
    
    # Run with error handling
    try:
        app.run(host='0.0.0.0', port=8083, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        exit(1)