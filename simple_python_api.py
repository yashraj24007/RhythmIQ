"""
Simplified Python API for testing
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

app = Flask(__name__)
CORS(app)

# Simple ECG API class
class SimpleECGAPI:
    def __init__(self):
        self.model = None
        self.class_names = ['F', 'M', 'N', 'Q', 'S', 'V']
        self.class_descriptions = {
            'N': 'Normal beat (sinus rhythm)',
            'S': 'Supraventricular beat (atrial premature)',
            'V': 'Ventricular beat (PVC - Premature Ventricular Contraction)',
            'F': 'Fusion beat (ventricular + normal)',
            'Q': 'Unknown/Paced beat',
            'M': 'Myocardial Infarction'
        }
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model"""
        try:
            model_path = '05_trained_models/rythmguard_model.joblib'
            if os.path.exists(model_path):
                loaded_data = joblib.load(model_path)
                
                if isinstance(loaded_data, dict) and 'model' in loaded_data:
                    self.model = loaded_data['model']
                    if 'class_names' in loaded_data:
                        self.class_names = loaded_data['class_names']
                    print(f"✅ Loaded ECG model from dictionary")
                else:
                    self.model = loaded_data
                    print(f"✅ Loaded ECG model directly")
                return True
            else:
                print(f"❌ Model file not found: {model_path}")
                return False
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            traceback.print_exc()
            return False
    
    def preprocess_image(self, image_path):
        """Simple image preprocessing"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                pil_image = Image.open(image_path)
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Resize and convert to grayscale
            image = cv2.resize(image, (224, 224))
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Flatten for Random Forest
            return image.flatten().reshape(1, -1)
        except Exception as e:
            print(f"Error preprocessing: {e}")
            return None
    
    def predict(self, image_path):
        """Make prediction"""
        try:
            if self.model is None:
                return {'error': 'Model not loaded', 'success': False}
            
            # Preprocess
            processed = self.preprocess_image(image_path)
            if processed is None:
                return {'error': 'Failed to preprocess', 'success': False}
            
            # Predict
            prediction = self.model.predict(processed)[0]
            probabilities = self.model.predict_proba(processed)[0]
            
            # Get class name
            if isinstance(prediction, (int, np.integer)):
                predicted_class = self.class_names[prediction]
            else:
                predicted_class = str(prediction)
            
            confidence = float(np.max(probabilities))
            
            return {
                'success': True,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.1f}%",
                'description': self.class_descriptions.get(predicted_class, 'Unknown'),
                'severity': 'moderate',  # Simplified
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            traceback.print_exc()
            return {'error': f'Prediction failed: {str(e)}', 'success': False}

# Initialize API
ecg_api = SimpleECGAPI()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': ecg_api.model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/analyze', methods=['POST'])
def analyze_ecg():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided', 'success': False}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            result = ecg_api.predict(temp_path)
            result['filename'] = file.filename
            return jsonify(result)
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    except Exception as e:
        print(f"Error in analyze_ecg: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}', 'success': False}), 500

if __name__ == '__main__':
    print("🫀 Simple RhythmIQ Python API")
    print("=" * 50)
    
    if not ecg_api.model:
        print("❌ Failed to load model")
        exit(1)
    
    print("✅ Model loaded successfully!")
    print("🚀 Starting API server on http://localhost:8083")
    
    app.run(host='0.0.0.0', port=8083, debug=False)