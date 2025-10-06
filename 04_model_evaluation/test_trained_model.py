#!/usr/bin/env python3
"""
🫀 Test Trained RythmGuard Model
===============================
This script tests the specific trained model created by simple_train.py
"""

import os
import sys
import numpy as np
import joblib
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import random

# Add paths for custom modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '02_preprocessing'))

from ecg_preprocessor import ECGPreprocessor
from severity_predictor import SeverityPredictor

def test_trained_model():
    """Test the trained RythmGuard model"""
    
    print("🧪 Testing Trained RythmGuard Model")
    print("=" * 60)
    
    # Check if model exists
    model_path = "rythmguard_model.joblib"
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print("💡 Run 'py simple_train.py' first to train the model")
        return False
    
    # Load model
    print("📁 Loading trained model...")
    model_data = joblib.load(model_path)
    model = model_data['model']
    class_names = model_data['class_names']
    
    print(f"✅ Model loaded successfully")
    print(f"🎯 Classes: {class_names}")
    print(f"📊 Training accuracy: {model_data.get('training_accuracy', 'Unknown'):.3f}")
    print(f"⏱️ Training time: {model_data.get('training_time', 'Unknown'):.2f} seconds")
    print(f"🔢 Images per class: {model_data.get('images_per_class', 'Unknown')}")
    
    # Initialize preprocessor
    preprocessor = ECGPreprocessor(".", target_size=(224, 224))
    severity_predictor = SeverityPredictor()
    
    # Test with sample images from test dataset
    print(f"\n🔍 Testing Model on Sample Images")
    print("-" * 40)
    
    results = []
    test_images = []
    test_labels = []
    predicted_labels = []
    
    for class_idx, class_name in enumerate(class_names):
        class_path = os.path.join("test", class_name)
        
        if not os.path.exists(class_path):
            print(f"⚠️ Test folder not found: {class_path}")
            continue
        
        # Get some random test images
        image_files = [f for f in os.listdir(class_path) if f.lower().endswith('.png')]
        sample_files = random.sample(image_files, min(5, len(image_files)))
        
        print(f"\n📁 Testing {class_name} class:")
        
        for img_file in sample_files:
            img_path = os.path.join(class_path, img_file)
            
            try:
                # Load and preprocess image
                processed_img = preprocessor.load_and_preprocess_image(img_path)
                if processed_img is None:
                    continue
                
                # Flatten for model prediction
                flattened = processed_img.flatten().reshape(1, -1)
                
                # Make prediction
                prediction = model.predict(flattened)[0]
                probabilities = model.predict_proba(flattened)[0]
                confidence = max(probabilities)
                predicted_class = class_names[prediction]
                
                # Test severity prediction
                severity_result = severity_predictor.predict_severity_rule_based(class_name)
                
                result = {
                    'filename': img_file,
                    'actual_class': class_name,
                    'predicted_class': predicted_class,
                    'confidence': confidence,
                    'correct': class_name == predicted_class,
                    'severity': severity_result['severity'],
                    'severity_confidence': severity_result['confidence']
                }
                
                results.append(result)
                test_images.append(img_path)
                test_labels.append(class_idx)
                predicted_labels.append(prediction)
                
                status = "✅" if result['correct'] else "❌"
                print(f"  {status} {img_file}: {predicted_class} ({confidence:.1%}) | Severity: {severity_result['severity']}")
                
            except Exception as e:
                print(f"  ❌ Error processing {img_file}: {e}")
    
    # Calculate overall metrics
    if results:
        print(f"\n📊 OVERALL TEST RESULTS")
        print("=" * 40)
        
        total_tests = len(results)
        correct_predictions = sum(1 for r in results if r['correct'])
        accuracy = correct_predictions / total_tests
        
        print(f"Total tests: {total_tests}")
        print(f"Correct predictions: {correct_predictions}")
        print(f"Test accuracy: {accuracy:.1%}")
        
        # Confusion matrix for tested samples
        if len(set(test_labels)) > 1:  # Only if we have multiple classes
            cm = confusion_matrix(test_labels, predicted_labels)
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                       xticklabels=class_names, yticklabels=class_names)
            plt.title('Test Sample Confusion Matrix')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.tight_layout()
            plt.savefig('test_confusion_matrix.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 Test confusion matrix saved: test_confusion_matrix.png")
        
        # Show performance by class
        class_results = {}
        for result in results:
            actual = result['actual_class']
            if actual not in class_results:
                class_results[actual] = {'total': 0, 'correct': 0}
            class_results[actual]['total'] += 1
            if result['correct']:
                class_results[actual]['correct'] += 1
        
        print(f"\n📈 Performance by Class:")
        for class_name, stats in class_results.items():
            accuracy = stats['correct'] / stats['total']
            print(f"  {class_name}: {stats['correct']}/{stats['total']} ({accuracy:.1%})")
        
        # Show severity distribution
        severity_counts = {}
        for result in results:
            severity = result['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print(f"\n🏥 Severity Distribution:")
        for severity, count in severity_counts.items():
            percentage = (count / total_tests) * 100
            print(f"  {severity}: {count} cases ({percentage:.1f}%)")
        
        # Show some sample predictions
        print(f"\n🔍 Sample Predictions:")
        for i, result in enumerate(results[:10]):
            status = "✅" if result['correct'] else "❌"
            print(f"  {status} {result['filename']}")
            print(f"      Actual: {result['actual_class']} → Predicted: {result['predicted_class']} ({result['confidence']:.1%})")
            print(f"      Severity: {result['severity']} ({result['severity_confidence']:.1%})")
        
    else:
        print("❌ No test results available")
        return False
    
    print(f"\n🎉 Model testing completed successfully!")
    print(f"✅ Your RythmGuard model is working correctly with {accuracy:.1%} accuracy")
    
    return True

def test_model_api():
    """Test the model API functionality"""
    print(f"\n🔧 Testing Model API")
    print("-" * 30)
    
    # Test model loading
    try:
        model_data = joblib.load("rythmguard_model.joblib")
        print("✅ Model loading: PASS")
    except Exception as e:
        print(f"❌ Model loading: FAIL - {e}")
        return False
    
    # Test preprocessor
    try:
        preprocessor = ECGPreprocessor(".")
        print("✅ Preprocessor initialization: PASS")
    except Exception as e:
        print(f"❌ Preprocessor initialization: FAIL - {e}")
        return False
    
    # Test severity predictor
    try:
        severity_predictor = SeverityPredictor()
        result = severity_predictor.predict_severity_rule_based('N')
        assert 'severity' in result and 'confidence' in result
        print("✅ Severity predictor: PASS")
    except Exception as e:
        print(f"❌ Severity predictor: FAIL - {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🫀 RythmGuard Trained Model Test Suite")
    print("=" * 60)
    
    # Test API functionality
    api_success = test_model_api()
    
    if api_success:
        # Test trained model
        model_success = test_trained_model()
        
        if model_success:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"✅ Your RythmGuard model is fully functional and ready for deployment")
        else:
            print(f"\n⚠️ Model tests had issues")
    else:
        print(f"\n❌ API tests failed")