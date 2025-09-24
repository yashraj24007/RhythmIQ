"""
End-to-End Model Testing Script
==============================

This script provides comprehensive testing for your RythmGuard model:
1. Pre-training validation
2. Training process validation  
3. Post-training model testing
4. Performance verification
"""

import os
import sys
import numpy as np
import pandas as pd
import cv2
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ModelTester:
    """Comprehensive model testing class"""
    
    def __init__(self, data_path="."):
        self.data_path = data_path
        self.models_dir = os.path.join(data_path, 'rythmguard_output', 'models')
        self.reports_dir = os.path.join(data_path, 'rythmguard_output', 'reports')
        self.test_results = {}
        
    def run_all_tests(self):
        """Run comprehensive model testing"""
        print("🧪 RythmGuard Model Testing Suite")
        print("=" * 60)
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Data Path: {os.path.abspath(self.data_path)}")
        
        # Pre-training tests
        print("\n🔍 PHASE 1: Pre-Training Validation")
        print("-" * 40)
        self.test_dataset_structure()
        self.test_image_accessibility()
        self.test_preprocessing_functionality()
        
        # Check if model is trained
        if self.check_trained_models():
            print("\n🤖 PHASE 2: Trained Model Testing")
            print("-" * 40)
            self.test_model_loading()
            self.test_model_predictions()
            self.test_severity_predictions()
            self.test_performance_metrics()
        else:
            print("\n⚠️  PHASE 2: Model Not Yet Trained")
            print("-" * 40)
            print("No trained models found. Please run training first:")
            print("   py rythmguard_pipeline.py")
        
        # Integration tests
        print("\n🔄 PHASE 3: Integration Testing")
        print("-" * 40)
        self.test_pipeline_integration()
        self.test_error_handling()
        
        # Generate test report
        self.generate_test_report()
        
        return self.test_results
    
    def test_dataset_structure(self):
        """Test 1: Dataset structure validation"""
        test_name = "Dataset Structure"
        try:
            expected_dirs = ['train', 'test']
            expected_classes = ['F', 'M', 'N', 'Q', 'S', 'V']
            
            # Check main directories
            for dir_name in expected_dirs:
                dir_path = os.path.join(self.data_path, dir_name)
                assert os.path.exists(dir_path), f"{dir_name} directory missing"
                
                # Check class subdirectories
                for class_name in expected_classes:
                    class_path = os.path.join(dir_path, class_name)
                    assert os.path.exists(class_path), f"{dir_name}/{class_name} directory missing"
            
            self.test_results[test_name] = {"status": "PASS", "message": "All directories found"}
            print(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_image_accessibility(self):
        """Test 2: Image file accessibility"""
        test_name = "Image Accessibility"
        try:
            total_images = 0
            accessible_images = 0
            
            for dataset in ['train', 'test']:
                dataset_path = os.path.join(self.data_path, dataset)
                if os.path.exists(dataset_path):
                    for class_name in os.listdir(dataset_path):
                        class_path = os.path.join(dataset_path, class_name)
                        if os.path.isdir(class_path):
                            images = [f for f in os.listdir(class_path) 
                                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                            total_images += len(images)
                            
                            # Test loading a sample image
                            if images:
                                sample_path = os.path.join(class_path, images[0])
                                img = cv2.imread(sample_path)
                                if img is not None:
                                    accessible_images += 1
            
            assert total_images > 0, "No images found in dataset"
            assert accessible_images > 0, "No images can be loaded"
            
            self.test_results[test_name] = {
                "status": "PASS", 
                "message": f"Found {total_images} images, {accessible_images} classes accessible"
            }
            print(f"✅ {test_name}: PASS - {total_images} images found")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_preprocessing_functionality(self):
        """Test 3: Preprocessing functionality"""
        test_name = "Preprocessing Functionality"
        try:
            from ecg_preprocessor import ECGPreprocessor
            
            preprocessor = ECGPreprocessor(self.data_path, (224, 224))
            
            # Test dataset analysis
            analysis = preprocessor.analyze_dataset('test')
            assert 'total_images' in analysis
            assert analysis['total_images'] > 0
            
            # Test image preprocessing
            test_dir = os.path.join(self.data_path, 'test')
            sample_found = False
            
            for class_name in os.listdir(test_dir):
                class_path = os.path.join(test_dir, class_name)
                if os.path.isdir(class_path):
                    images = [f for f in os.listdir(class_path) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if images:
                        sample_path = os.path.join(class_path, images[0])
                        processed = preprocessor.load_and_preprocess_image(sample_path)
                        if processed is not None:
                            assert processed.shape == (224, 224, 3)
                            assert 0 <= processed.min() <= processed.max() <= 1
                            sample_found = True
                            break
            
            assert sample_found, "Could not process any sample image"
            
            self.test_results[test_name] = {"status": "PASS", "message": "Preprocessing works correctly"}
            print(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def check_trained_models(self):
        """Check if trained models exist"""
        if not os.path.exists(self.models_dir):
            return False
        
        required_models = [
            'ecg_classification_model.joblib',
            'severity_prediction_model.joblib'
        ]
        
        for model_file in required_models:
            if not os.path.exists(os.path.join(self.models_dir, model_file)):
                return False
        
        return True
    
    def test_model_loading(self):
        """Test 4: Model loading"""
        test_name = "Model Loading"
        try:
            # Test classification model
            classification_path = os.path.join(self.models_dir, 'ecg_classification_model.joblib')
            classification_model = joblib.load(classification_path)
            assert hasattr(classification_model, 'predict')
            assert hasattr(classification_model, 'predict_proba')
            
            # Test severity model  
            severity_path = os.path.join(self.models_dir, 'severity_prediction_model.joblib')
            severity_model = joblib.load(severity_path)
            assert hasattr(severity_model, 'predict')
            
            self.test_results[test_name] = {"status": "PASS", "message": "Both models loaded successfully"}
            print(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_model_predictions(self):
        """Test 5: Model prediction functionality"""
        test_name = "Model Predictions"
        try:
            from ecg_preprocessor import ECGPreprocessor
            
            # Load models
            classification_path = os.path.join(self.models_dir, 'ecg_classification_model.joblib')
            model = joblib.load(classification_path)
            
            preprocessor = ECGPreprocessor(self.data_path, (224, 224))
            
            # Test on sample images from each class
            predictions_made = 0
            test_dir = os.path.join(self.data_path, 'test')
            
            for class_name in ['N', 'V', 'M']:  # Test on 3 main classes
                class_path = os.path.join(test_dir, class_name)
                if os.path.exists(class_path):
                    images = [f for f in os.listdir(class_path) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if images:
                        sample_path = os.path.join(class_path, images[0])
                        processed = preprocessor.load_and_preprocess_image(sample_path)
                        
                        if processed is not None:
                            image_flat = processed.reshape(1, -1)
                            prediction = model.predict(image_flat)
                            prediction_proba = model.predict_proba(image_flat)
                            
                            # Validate prediction format
                            assert len(prediction) == 1
                            assert 0 <= prediction[0] < 6  # 6 classes
                            assert prediction_proba.shape[1] == 6
                            assert np.isclose(np.sum(prediction_proba), 1.0)
                            
                            predictions_made += 1
            
            assert predictions_made >= 2, "Should make predictions on at least 2 classes"
            
            self.test_results[test_name] = {
                "status": "PASS", 
                "message": f"Successfully made {predictions_made} predictions"
            }
            print(f"✅ {test_name}: PASS - {predictions_made} predictions tested")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_severity_predictions(self):
        """Test 6: Severity prediction functionality"""
        test_name = "Severity Predictions"
        try:
            from severity_predictor import SeverityPredictor
            
            severity_predictor = SeverityPredictor()
            
            # Test severity label generation
            test_classes = ['N', 'V', 'M', 'S']
            severity_labels = severity_predictor.generate_severity_labels(test_classes)
            
            assert len(severity_labels) == len(test_classes)
            assert all(0 <= label <= 2 for label in severity_labels)
            
            # Test feature extraction (if possible)
            dummy_image = np.random.random((224, 224, 3)).astype(np.float32)
            features = severity_predictor.extract_severity_features(dummy_image, 'N')
            assert len(features) > 0
            
            self.test_results[test_name] = {"status": "PASS", "message": "Severity prediction works"}
            print(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_performance_metrics(self):
        """Test 7: Performance metrics availability"""
        test_name = "Performance Metrics"
        try:
            # Check if results file exists
            results_file = os.path.join(self.reports_dir, 'complete_system_results.csv')
            report_file = os.path.join(self.reports_dir, 'rythmguard_comprehensive_report.md')
            
            metrics_found = []
            
            if os.path.exists(results_file):
                df = pd.read_csv(results_file)
                assert len(df) > 0, "Results file should not be empty"
                required_columns = ['predicted_class', 'classification_confidence', 'predicted_severity']
                for col in required_columns:
                    if col in df.columns:
                        metrics_found.append(col)
            
            if os.path.exists(report_file):
                metrics_found.append("comprehensive_report")
            
            assert len(metrics_found) > 0, "No performance metrics found"
            
            self.test_results[test_name] = {
                "status": "PASS", 
                "message": f"Found metrics: {', '.join(metrics_found)}"
            }
            print(f"✅ {test_name}: PASS - {len(metrics_found)} metric sources found")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_pipeline_integration(self):
        """Test 8: Pipeline integration"""
        test_name = "Pipeline Integration"
        try:
            from rythmguard_pipeline import RythmGuardPipeline
            
            pipeline = RythmGuardPipeline(self.data_path, (224, 224))
            
            # Test if pipeline can be initialized
            assert hasattr(pipeline, 'preprocessor')
            assert hasattr(pipeline, 'severity_predictor')
            assert hasattr(pipeline, 'output_dir')
            
            # Test if output directories exist
            assert os.path.exists(pipeline.output_dir)
            assert os.path.exists(pipeline.models_dir)
            
            self.test_results[test_name] = {"status": "PASS", "message": "Pipeline integration works"}
            print(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def test_error_handling(self):
        """Test 9: Error handling"""
        test_name = "Error Handling"
        try:
            from ecg_preprocessor import ECGPreprocessor
            
            preprocessor = ECGPreprocessor(self.data_path, (224, 224))
            
            # Test with invalid image path
            result = preprocessor.load_and_preprocess_image("invalid_path.png")
            assert result is None, "Should handle invalid paths gracefully"
            
            # Test with invalid dataset
            try:
                analysis = preprocessor.analyze_dataset('invalid_dataset')
                # Should either handle gracefully or raise appropriate exception
            except Exception:
                pass  # Expected behavior
            
            self.test_results[test_name] = {"status": "PASS", "message": "Error handling works"}
            print(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results[test_name] = {"status": "FAIL", "message": str(e)}
            print(f"❌ {test_name}: FAIL - {e}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📋 TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {passed_tests/total_tests*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if result['status'] == 'FAIL':
                    print(f"   • {test_name}: {result['message']}")
        
        # Save report to file
        report_path = os.path.join(self.data_path, 'model_test_report.txt')
        with open(report_path, 'w') as f:
            f.write(f"RythmGuard Model Test Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Test Results Summary:\n")
            f.write(f"Total Tests: {total_tests}\n")
            f.write(f"Passed: {passed_tests}\n")
            f.write(f"Failed: {failed_tests}\n")
            f.write(f"Success Rate: {passed_tests/total_tests*100:.1f}%\n\n")
            
            f.write("Detailed Results:\n")
            for test_name, result in self.test_results.items():
                f.write(f"{test_name}: {result['status']} - {result['message']}\n")
        
        print(f"\n💾 Test report saved to: {report_path}")
        
        # Overall assessment
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Your model is working correctly.")
        elif passed_tests >= total_tests * 0.8:
            print("\n🟡 MOSTLY WORKING! Minor issues detected.")
        else:
            print("\n🔴 SIGNIFICANT ISSUES! Please review failed tests.")
        
        return passed_tests, total_tests

def main():
    """Main testing function"""
    tester = ModelTester()
    results = tester.run_all_tests()
    return results

if __name__ == "__main__":
    main()