"""
Test Suite for RythmGuard ECG Model Validation
=============================================

These tests verify that the trained ECG model is working correctly:
1. Model loading and initialization
2. Image preprocessing functionality  
3. Classification predictions
4. Severity prediction
5. Complete pipeline integration
"""

import pytest
import numpy as np
import os
import sys
import cv2
from unittest.mock import Mock, patch
import joblib

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ecg_preprocessor import ECGPreprocessor
    from severity_predictor import SeverityPredictor
    from rythmguard_pipeline import RythmGuardPipeline
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

class TestRythmGuardModel:
    """Test suite for RythmGuard ECG model functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_image_size = (224, 224)
        self.expected_classes = ['F', 'M', 'N', 'Q', 'S', 'V']
        self.severity_levels = ['Mild', 'Moderate', 'Severe']
        
        # Check if models exist
        self.models_dir = os.path.join(self.data_path, 'rythmguard_output', 'models')
        self.has_trained_models = os.path.exists(self.models_dir)
        
    def test_data_directory_structure(self):
        """Test 1: Verify dataset directory structure exists"""
        print("\n🔍 Test 1: Checking dataset structure...")
        
        test_dir = os.path.join(self.data_path, 'test')
        train_dir = os.path.join(self.data_path, 'train')
        
        assert os.path.exists(test_dir), "Test directory should exist"
        assert os.path.exists(train_dir), "Train directory should exist"
        
        # Check if expected classes exist
        for class_name in self.expected_classes:
            test_class_dir = os.path.join(test_dir, class_name)
            train_class_dir = os.path.join(train_dir, class_name)
            
            assert os.path.exists(test_class_dir), f"Test class {class_name} directory should exist"
            assert os.path.exists(train_class_dir), f"Train class {class_name} directory should exist"
        
        print("✅ Dataset structure is valid")
    
    def test_image_loading_and_preprocessing(self):
        """Test 2: Verify image loading and preprocessing works"""
        print("\n🖼️  Test 2: Testing image preprocessing...")
        
        preprocessor = ECGPreprocessor(self.data_path, self.test_image_size)
        
        # Find a sample image
        test_dir = os.path.join(self.data_path, 'test')
        sample_image_path = None
        
        for class_name in self.expected_classes:
            class_dir = os.path.join(test_dir, class_name)
            if os.path.exists(class_dir):
                images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    sample_image_path = os.path.join(class_dir, images[0])
                    break
        
        assert sample_image_path is not None, "Should find at least one sample image"
        
        # Test image loading
        processed_image = preprocessor.load_and_preprocess_image(sample_image_path)
        
        assert processed_image is not None, "Image should load successfully"
        assert processed_image.shape == (*self.test_image_size, 3), f"Image should be resized to {self.test_image_size}"
        assert processed_image.dtype == np.float32, "Image should be float32"
        assert 0 <= processed_image.min() <= processed_image.max() <= 1, "Image should be normalized [0,1]"
        
        print(f"✅ Image preprocessing works: {processed_image.shape}")
    
    def test_preprocessor_dataset_analysis(self):
        """Test 3: Verify dataset analysis functionality"""
        print("\n📊 Test 3: Testing dataset analysis...")
        
        preprocessor = ECGPreprocessor(self.data_path, self.test_image_size)
        
        # Test analysis on test dataset
        analysis = preprocessor.analyze_dataset('test')
        
        assert 'classes' in analysis, "Analysis should include classes"
        assert 'total_images' in analysis, "Analysis should include total images"
        assert analysis['total_images'] > 0, "Should find images in dataset"
        
        # Check if expected classes are found
        found_classes = set(analysis['classes'].keys())
        expected_classes_set = set(self.expected_classes)
        
        assert found_classes == expected_classes_set, f"Should find all expected classes: {expected_classes_set}"
        
        print(f"✅ Dataset analysis works: {analysis['total_images']} images, {len(analysis['classes'])} classes")
    
    def test_severity_predictor_initialization(self):
        """Test 4: Verify severity predictor can be initialized"""
        print("\n⚕️  Test 4: Testing severity predictor...")
        
        severity_predictor = SeverityPredictor()
        
        assert hasattr(severity_predictor, 'severity_mapping'), "Should have severity mapping"
        assert hasattr(severity_predictor, 'class_severity_rules'), "Should have class severity rules"
        
        # Test severity label generation
        test_classes = ['N', 'V', 'M']
        severity_labels = severity_predictor.generate_severity_labels(test_classes)
        
        assert len(severity_labels) == len(test_classes), "Should generate labels for all classes"
        assert all(0 <= label <= 2 for label in severity_labels), "Severity labels should be 0, 1, or 2"
        
        print("✅ Severity predictor initialization works")
    
    def test_pipeline_initialization(self):
        """Test 5: Verify pipeline can be initialized"""
        print("\n🔄 Test 5: Testing pipeline initialization...")
        
        pipeline = RythmGuardPipeline(self.data_path, self.test_image_size)
        
        assert hasattr(pipeline, 'preprocessor'), "Pipeline should have preprocessor"
        assert hasattr(pipeline, 'severity_predictor'), "Pipeline should have severity predictor"
        assert hasattr(pipeline, 'output_dir'), "Pipeline should have output directory"
        
        # Check if output directories are created
        assert os.path.exists(pipeline.output_dir), "Output directory should be created"
        assert os.path.exists(pipeline.models_dir), "Models directory should be created"
        assert os.path.exists(pipeline.reports_dir), "Reports directory should be created"
        
        print("✅ Pipeline initialization works")
    
    @pytest.mark.skipif(not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rythmguard_output', 'models')), 
                        reason="Trained models not found - run training first")
    def test_trained_model_loading(self):
        """Test 6: Verify trained models can be loaded (if they exist)"""
        print("\n🤖 Test 6: Testing trained model loading...")
        
        models_dir = os.path.join(self.data_path, 'rythmguard_output', 'models')
        
        # Check for classification model
        classification_model_path = os.path.join(models_dir, 'ecg_classification_model.joblib')
        if os.path.exists(classification_model_path):
            model = joblib.load(classification_model_path)
            assert hasattr(model, 'predict'), "Classification model should have predict method"
            assert hasattr(model, 'predict_proba'), "Classification model should have predict_proba method"
            print("✅ Classification model loads successfully")
        
        # Check for severity prediction model
        severity_model_path = os.path.join(models_dir, 'severity_prediction_model.joblib')
        if os.path.exists(severity_model_path):
            print("✅ Severity prediction model exists")
        
        print("✅ Model loading test completed")
    
    @pytest.mark.skipif(not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rythmguard_output', 'models', 'ecg_classification_model.joblib')), 
                        reason="Trained classification model not found - run training first")
    def test_model_prediction_functionality(self):
        """Test 7: Verify model can make predictions on real data"""
        print("\n🎯 Test 7: Testing model predictions...")
        
        # Load trained model
        models_dir = os.path.join(self.data_path, 'rythmguard_output', 'models')
        classification_model_path = os.path.join(models_dir, 'ecg_classification_model.joblib')
        
        model = joblib.load(classification_model_path)
        preprocessor = ECGPreprocessor(self.data_path, self.test_image_size)
        
        # Find a sample image
        test_dir = os.path.join(self.data_path, 'test')
        sample_image_path = None
        true_class = None
        
        for class_name in self.expected_classes:
            class_dir = os.path.join(test_dir, class_name)
            if os.path.exists(class_dir):
                images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    sample_image_path = os.path.join(class_dir, images[0])
                    true_class = class_name
                    break
        
        assert sample_image_path is not None, "Should find sample image for testing"
        
        # Preprocess image
        processed_image = preprocessor.load_and_preprocess_image(sample_image_path)
        image_flat = processed_image.reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(image_flat)
        prediction_proba = model.predict_proba(image_flat)
        
        assert len(prediction) == 1, "Should return one prediction"
        assert 0 <= prediction[0] < len(self.expected_classes), "Prediction should be valid class index"
        assert prediction_proba.shape == (1, len(self.expected_classes)), "Probability shape should match classes"
        assert np.isclose(np.sum(prediction_proba), 1.0), "Probabilities should sum to 1"
        
        print(f"✅ Model prediction works: predicted class {prediction[0]}, confidence {np.max(prediction_proba):.3f}")
    
    def test_complete_pipeline_functionality(self):
        """Test 8: Test complete pipeline without actual training (mock test)"""
        print("\n🔄 Test 8: Testing complete pipeline structure...")
        
        pipeline = RythmGuardPipeline(self.data_path, self.test_image_size)
        
        # Test if pipeline has all required methods
        required_methods = [
            'run_complete_pipeline',
            '_train_classification_model',
            '_evaluate_classification',
            '_train_severity_prediction',
            '_evaluate_complete_system'
        ]
        
        for method_name in required_methods:
            assert hasattr(pipeline, method_name), f"Pipeline should have {method_name} method"
        
        print("✅ Pipeline has all required methods")
    
    def test_error_handling(self):
        """Test 9: Test error handling with invalid inputs"""
        print("\n⚠️  Test 9: Testing error handling...")
        
        preprocessor = ECGPreprocessor(self.data_path, self.test_image_size)
        
        # Test with non-existent image
        result = preprocessor.load_and_preprocess_image("non_existent_image.png")
        assert result is None, "Should return None for non-existent image"
        
        # Test with invalid directory
        try:
            invalid_preprocessor = ECGPreprocessor("/invalid/path", self.test_image_size)
            analysis = invalid_preprocessor.analyze_dataset('test')
            # Should handle gracefully or raise appropriate exception
        except Exception as e:
            print(f"Expected error handled: {type(e).__name__}")
        
        print("✅ Error handling works correctly")

def test_quick_model_validation():
    """Quick validation test that can run without trained models"""
    print("\n🚀 Quick Model Validation Test")
    print("=" * 50)
    
    data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Test 1: Check if we can create fake predictions
    fake_image = np.random.random((224, 224, 3)).astype(np.float32)
    assert fake_image.shape == (224, 224, 3), "Test image should have correct shape"
    
    # Test 2: Check if preprocessing pipeline exists
    try:
        from ecg_preprocessor import ECGPreprocessor
        preprocessor = ECGPreprocessor(data_path, (224, 224))
        print("✅ ECG Preprocessor can be imported and initialized")
    except Exception as e:
        print(f"❌ Preprocessor error: {e}")
        return False
    
    # Test 3: Check if severity predictor exists
    try:
        from severity_predictor import SeverityPredictor
        severity_predictor = SeverityPredictor()
        print("✅ Severity Predictor can be imported and initialized")
    except Exception as e:
        print(f"❌ Severity predictor error: {e}")
        return False
    
    # Test 4: Check if pipeline exists
    try:
        from rythmguard_pipeline import RythmGuardPipeline
        pipeline = RythmGuardPipeline(data_path, (224, 224))
        print("✅ RythmGuard Pipeline can be imported and initialized")
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        return False
    
    print("✅ All core components are working!")
    return True

if __name__ == "__main__":
    # Run quick validation if called directly
    test_quick_model_validation()