"""
RhythmIQ Python API Service
==========================

Flask API service that wraps the trained ECG ML model for integration with Java web app.
"""

import os
import sys
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from PIL import Image
import cv2
import tempfile
import traceback
from datetime import datetime

# Add the project directories to Python path
sys.path.append('02_preprocessing')
sys.path.append('03_model_training')

try:
    from ecg_preprocessor import ECGPreprocessor
    from severity_predictor import SeverityPredictor
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    print("Make sure you're running from the project root directory")

app = Flask(__name__)
CORS(app)  # Enable CORS for Java web app integration

class ECGAnalysisAPI:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.severity_predictor = None
        self.class_names = ['N', 'S', 'V', 'F', 'Q', 'M']
        self.class_descriptions = {
            'N': 'Normal beat (sinus rhythm)',
            'S': 'Supraventricular beat (atrial premature)',
            'V': 'Ventricular beat (PVC - Premature Ventricular Contraction)',
            'F': 'Fusion beat (ventricular + normal)',
            'Q': 'Unknown/Paced beat',
            'M': 'Myocardial Infarction'
        }
        self.load_models()
    
    def load_models(self):
        """Load the trained ML models"""
        try:
            # Load the main ECG classification model
            model_path = '05_trained_models/rythmguard_model.joblib'
            if os.path.exists(model_path):
                loaded_data = joblib.load(model_path)
                
                # Handle both direct model and dictionary format
                if isinstance(loaded_data, dict) and 'model' in loaded_data:
                    self.model = loaded_data['model']
                    # Also load class names from the saved data if available
                    if 'class_names' in loaded_data:
                        self.class_names = loaded_data['class_names']
                    print(f"✅ Loaded ECG model from dictionary in {model_path}")
                else:
                    self.model = loaded_data
                    print(f"✅ Loaded ECG model directly from {model_path}")
            else:
                print(f"❌ Model file not found: {model_path}")
                return False
            
            # Initialize preprocessor
            data_path = '01_data'
            if os.path.exists(data_path):
                self.preprocessor = ECGPreprocessor(data_path, target_size=(224, 224))
                print("✅ Initialized ECG preprocessor")
            else:
                print(f"❌ Data path not found: {data_path}")
            
            # Initialize severity predictor
            self.severity_predictor = SeverityPredictor()
            print("✅ Initialized severity predictor")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            traceback.print_exc()
            return False
    
    def preprocess_image(self, image_path):
        """Preprocess a single ECG image for prediction"""
        try:
            # Load and preprocess the image
            image = cv2.imread(image_path)
            if image is None:
                # Try with PIL for different formats
                pil_image = Image.open(image_path)
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Resize to target size
            image = cv2.resize(image, (224, 224))
            
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Flatten for the Random Forest model
            image_flattened = image.flatten()
            
            return image_flattened.reshape(1, -1), image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None, None
    
    def predict_ecg(self, image_path):
        """Predict ECG classification and severity"""
        try:
            if self.model is None:
                return {
                    'error': 'Model not loaded',
                    'success': False
                }
            
            # Preprocess the image
            processed_image, original_image = self.preprocess_image(image_path)
            if processed_image is None:
                return {
                    'error': 'Failed to preprocess image',
                    'success': False
                }
            
            # Make prediction
            prediction = self.model.predict(processed_image)[0]
            prediction_proba = self.model.predict_proba(processed_image)[0]
            
            # Get the predicted class
            if isinstance(prediction, (int, np.integer)):
                predicted_class = self.class_names[prediction]
            else:
                predicted_class = str(prediction)
            
            # Get confidence score
            confidence = float(np.max(prediction_proba))
            
            # Predict severity using the severity predictor
            try:
                severity_label, severity_confidence, severity_name = self.severity_predictor.predict_severity(
                    original_image, predicted_class
                )
            except:
                # Fallback severity prediction
                severity_rules = {
                    'N': 'mild',
                    'S': 'moderate', 
                    'V': 'moderate',
                    'F': 'severe',
                    'Q': 'moderate',
                    'M': 'severe'
                }
                severity_name = severity_rules.get(predicted_class, 'moderate')
                severity_confidence = confidence * 0.8
            
            # Format result
            result = {
                'success': True,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.1f}%",
                'description': self.class_descriptions.get(predicted_class, 'Unknown'),
                'severity': severity_name,
                'severity_confidence': float(severity_confidence),
                'analysis_time': datetime.now().isoformat(),
                'all_probabilities': {
                    self.class_names[i]: float(prob) 
                    for i, prob in enumerate(prediction_proba)
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            traceback.print_exc()
            return {
                'error': f'Prediction failed: {str(e)}',
                'success': False
            }

# Initialize the API
ecg_api = ECGAnalysisAPI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': ecg_api.model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/analyze', methods=['POST'])
def analyze_ecg():
    """Main ECG analysis endpoint"""
    try:
        # Check if file is provided
        if 'image' not in request.files:
            return jsonify({
                'error': 'No image file provided',
                'success': False
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'success': False
            }), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Analyze the ECG
            result = ecg_api.predict_ecg(temp_path)
            result['filename'] = file.filename
            
            return jsonify(result)
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
    
    except Exception as e:
        print(f"Error in analyze_ecg: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'success': False
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    return jsonify({
        'model_loaded': ecg_api.model is not None,
        'classes': ecg_api.class_names,
        'descriptions': ecg_api.class_descriptions,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🫀 RhythmIQ Python API Service")
    print("=" * 50)
    
    if not ecg_api.model:
        print("❌ Failed to load models. Please check:")
        print("   1. Model file exists at: 05_trained_models/rythmguard_model.joblib")
        print("   2. Data directory exists at: 01_data/")
        print("   3. Required Python modules are available")
        sys.exit(1)
    
    print("✅ All models loaded successfully!")
    print("🚀 Starting API server on http://localhost:8083")
    print("🔗 Ready for integration with Java web app")
    print()
    
    app.run(host='0.0.0.0', port=8083, debug=False)