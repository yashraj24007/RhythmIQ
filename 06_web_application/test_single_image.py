#!/usr/bin/env python3
"""
Single ECG Image Analysis Script for Java Web Application
========================================================
This script analyzes a single ECG image and returns results in JSON format
for consumption by the Java web application.
"""

import sys
import json
import os
import numpy as np
import joblib
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Import your existing modules
try:
    import sys
    sys.path.append('../02_preprocessing')
    sys.path.append('../03_model_training')
    from ecg_preprocessor import ECGPreprocessor
    from severity_predictor import SeverityPredictor
except ImportError as e:
    print(json.dumps({
        "error": f"Failed to import required modules: {str(e)}",
        "success": False
    }))
    sys.exit(1)

def analyze_single_ecg(image_path):
    """
    Analyze a single ECG image and return results
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return {
                "error": f"Image file not found: {image_path}",
                "success": False
            }
        
        # Load the trained model
        model_path = "../05_trained_models/rythmguard_model.joblib"
        if not os.path.exists(model_path):
            return {
                "error": f"Model file not found: {model_path}",
                "success": False
            }
        
        # Load model and preprocessor
        model = joblib.load(model_path)
        preprocessor = ECGPreprocessor()
        severity_predictor = SeverityPredictor()
        
        # Load and preprocess image
        try:
            image = Image.open(image_path).convert('RGB')
            image_array = np.array(image)
            
            # Preprocess image
            processed_image = preprocessor.preprocess_single_image(image_array)
            
            # Reshape for model prediction
            processed_flat = processed_image.reshape(1, -1)
            
            # Make prediction
            prediction = model.predict(processed_flat)[0]
            probabilities = model.predict_proba(processed_flat)[0]
            
            # Get confidence
            confidence = float(np.max(probabilities) * 100)
            
            # Get class names
            class_names = model.classes_
            predicted_class = prediction
            
            # Predict severity
            severity_result = severity_predictor.predict_severity(predicted_class, confidence)
            severity = severity_result['severity']
            severity_confidence = severity_result['confidence']
            
            # Prepare results
            result = {
                "success": True,
                "filename": os.path.basename(image_path),
                "class": predicted_class,
                "confidence": confidence,
                "severity": severity,
                "severity_confidence": severity_confidence,
                "all_probabilities": {
                    str(class_names[i]): float(probabilities[i] * 100) 
                    for i in range(len(class_names))
                },
                "model_info": {
                    "classes": list(class_names),
                    "total_classes": len(class_names)
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "error": f"Image processing failed: {str(e)}",
                "success": False
            }
            
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "success": False
        }

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "Usage: python test_single_image.py <image_path>",
            "success": False
        }))
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Analyze the image
    result = analyze_single_ecg(image_path)
    
    # Output JSON result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if result.get("success", False):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()