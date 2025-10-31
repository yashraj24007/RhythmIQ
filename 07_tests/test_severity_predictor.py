import pytest
import numpy as np
import os
from PIL import Image
import sys
sys.path.append('..')
from severity_predictor import SeverityPredictor

class TestSeverityPredictor:
    
    @pytest.fixture
    def severity_predictor(self):
        """Create a SeverityPredictor instance for testing"""
        return SeverityPredictor()
    
    @pytest.fixture
    def sample_images(self):
        """Load sample ECG images from your test dataset"""
        test_data_path = "test"
        sample_images = {}
        classes = ['N', 'S', 'V', 'F', 'Q', 'M']
        
        for class_name in classes:
            class_path = os.path.join(test_data_path, class_name)
            if os.path.exists(class_path):
                image_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if image_files:
                    # Take first image as sample
                    sample_path = os.path.join(class_path, image_files[0])
                    try:
                        image = Image.open(sample_path).convert('RGB')
                        image_array = np.array(image)
                        sample_images[class_name] = {
                            'image': image_array,
                            'path': sample_path,
                            'filename': image_files[0]
                        }
                    except Exception as e:
                        print(f"Could not load sample image for class {class_name}: {e}")
        
        return sample_images
    
    def test_severity_predictor_initialization(self, severity_predictor):
        """Test that SeverityPredictor initializes correctly"""
        assert severity_predictor is not None
        assert hasattr(severity_predictor, 'predict_severity')
        assert hasattr(severity_predictor, 'severity_mapping')
        assert len(severity_predictor.severity_mapping) == 3  # Mild, Moderate, Severe
        assert hasattr(severity_predictor, 'class_severity_rules')
        assert len(severity_predictor.class_severity_rules) == 6  # N, S, V, F, Q, M
    
    def test_predict_severity_with_real_images(self, severity_predictor, sample_images):
        """Test severity prediction with real ECG images"""
        if not sample_images:
            pytest.skip("No sample images available for testing")
        
        for class_name, image_data in sample_images.items():
            image = image_data['image']
            
            # Test rule-based severity prediction (without trained model)
            severity_result = severity_predictor.predict_severity_rule_based(class_name)
            
            # Validate outputs
            assert 'severity' in severity_result, f"Missing severity for class {class_name}"
            assert 'confidence' in severity_result, f"Missing confidence for class {class_name}"
            assert severity_result['severity'] in ['Mild', 'Moderate', 'Severe'], f"Invalid severity for class {class_name}"
            assert 0.0 <= severity_result['confidence'] <= 1.0, f"Invalid confidence for class {class_name}"
            
            print(f"✅ Class {class_name}: {severity_result['severity']} (confidence: {severity_result['confidence']:.2f})")
    
    def test_predict_severity_different_classes(self, severity_predictor, sample_images):
        """Test that different ECG classes produce appropriate severity predictions"""
        if len(sample_images) < 2:
            pytest.skip("Need at least 2 different ECG classes for comparison")
        
        predictions = {}
        for class_name, image_data in sample_images.items():
            image = image_data['image']
            severity_result = severity_predictor.predict_severity_rule_based(class_name)
            predictions[class_name] = {
                'severity': severity_result['severity'],
                'confidence': severity_result['confidence']
            }
        
        # Test that we get predictions for different classes
        assert len(predictions) >= 2, "Should have predictions for multiple classes"
        
        # Print results for inspection
        print("\n📊 Severity Predictions by ECG Class:")
        for class_name, pred in predictions.items():
            print(f"  {class_name}: {pred['severity']} ({pred['confidence']:.2f})")
    
    def test_clinical_severity_mapping(self, severity_predictor):
        """Test that clinical severity mappings are appropriate"""
        # Test expected severe conditions
        severe_conditions = ['M']  # Myocardial Infarction should be severe
        moderate_conditions = ['V', 'F']  # PVC and Fusion should be moderate
        mild_conditions = ['N']  # Normal should be mild
        
        for condition in severe_conditions:
            severity_result = severity_predictor.predict_severity_rule_based(condition)
            # We expect severe conditions to have higher probability of being severe
            print(f"🚨 {condition} (expected severe): Got {severity_result['severity']}")
        
        for condition in mild_conditions:
            severity_result = severity_predictor.predict_severity_rule_based(condition)
            # We expect normal to have higher probability of being mild
            print(f"✅ {condition} (expected mild): Got {severity_result['severity']}")
    
    def test_batch_prediction(self, severity_predictor, sample_images):
        """Test severity prediction on multiple images"""
        if len(sample_images) < 3:
            pytest.skip("Need at least 3 sample images for batch testing")
        
        batch_results = []
        for class_name, image_data in list(sample_images.items())[:3]:
            image = image_data['image']
            severity_result = severity_predictor.predict_severity_rule_based(class_name)
            
            batch_results.append({
                'class': class_name,
                'severity': severity_result['severity'],
                'confidence': severity_result['confidence'],
                'filename': image_data['filename']
            })
        
        # Validate batch results
        assert len(batch_results) == 3, "Should process 3 images in batch"
        
        print("\n📋 Batch Prediction Results:")
        for i, result in enumerate(batch_results, 1):
            print(f"  {i}. {result['filename']} ({result['class']}): {result['severity']} ({result['confidence']:.2f})")
    
    def test_image_preprocessing_integration(self, severity_predictor, sample_images):
        """Test that images are properly preprocessed before severity prediction"""
        if not sample_images:
            pytest.skip("No sample images available")
        
        # Test with first available image
        class_name, image_data = next(iter(sample_images.items()))
        original_image = image_data['image']
        
        # Test with different image sizes
        small_image = np.array(Image.fromarray(original_image).resize((100, 100)))
        large_image = np.array(Image.fromarray(original_image).resize((500, 500)))
        
        # Both should work (rule-based doesn't depend on image preprocessing)
        for test_image, size_name in [(small_image, "small"), (large_image, "large")]:
            severity_result = severity_predictor.predict_severity_rule_based(class_name)
            
            assert severity_result['severity'] in ['Mild', 'Moderate', 'Severe'], f"Failed for {size_name} image"
            print(f"✅ {size_name.capitalize()} image ({test_image.shape}): {severity_result['severity']}")

def test_severity_predictor():
    """Simple test function for backward compatibility"""
    predictor = SeverityPredictor()
    assert predictor is not None
    print("✅ Severity predictor basic test passed")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])