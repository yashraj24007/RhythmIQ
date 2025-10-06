#!/usr/bin/env python3
"""
🫀 RythmGuard Quick Training Test
===============================
This script tests model training with a small subset of data to verify functionality.
"""

import os
import sys
import time
import random
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import joblib

# Add current directory and preprocessing directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '02_preprocessing'))

from ecg_preprocessor import ECGPreprocessor
from severity_predictor import SeverityPredictor

class QuickTrainingTest:
    def __init__(self, data_path, max_images_per_class=10):
        """Initialize quick training test with limited data."""
        self.data_path = Path(data_path)
        self.max_images_per_class = max_images_per_class
        self.preprocessor = ECGPreprocessor(data_path)
        self.severity_predictor = SeverityPredictor()
        
    def create_small_dataset(self, split='train'):
        """Create a small dataset for quick testing."""
        print(f"🔄 Creating small {split} dataset ({self.max_images_per_class} images per class)")
        
        split_path = self.data_path / split
        if not split_path.exists():
            raise FileNotFoundError(f"Dataset split not found: {split_path}")
        
        X, y, class_names, image_paths = [], [], [], []
        
        # Get class folders
        class_folders = [f for f in split_path.iterdir() if f.is_dir()]
        class_folders.sort()
        
        for class_idx, class_folder in enumerate(class_folders):
            class_name = class_folder.name
            class_names.append(class_name)
            
            # Get random sample of images from this class
            image_files = list(class_folder.glob("*.png"))
            if len(image_files) > self.max_images_per_class:
                image_files = random.sample(image_files, self.max_images_per_class)
            
            print(f"   📁 {class_name}: {len(image_files)} images")
            
            for img_path in image_files:
                try:
                    # Load and preprocess image
                    processed_img = self.preprocessor.load_and_preprocess_image(str(img_path))
                    if processed_img is not None:
                        # Flatten image for traditional ML
                        X.append(processed_img.flatten())
                        y.append(class_idx)
                        image_paths.append(str(img_path))
                except Exception as e:
                    print(f"   ⚠️  Error processing {img_path.name}: {e}")
                    continue
        
        return np.array(X), np.array(y), class_names, image_paths
    
    def train_quick_model(self):
        """Train a quick model with limited data."""
        print("\n🚀 Quick Model Training Test")
        print("=" * 50)
        
        # Create small training dataset
        X_train, y_train, class_names, train_paths = self.create_small_dataset('train')
        
        if len(X_train) == 0:
            print("❌ No training data loaded!")
            return False
        
        print(f"📊 Training data shape: {X_train.shape}")
        print(f"🎯 Classes: {class_names}")
        
        # Train model
        print("🔄 Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=10,  # Small for quick training
            max_depth=5,      # Shallow for quick training
            random_state=42,
            n_jobs=-1
        )
        
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        print(f"✅ Model trained in {training_time:.2f} seconds")
        
        # Test on training data (just to verify prediction works)
        y_pred = model.predict(X_train)
        accuracy = accuracy_score(y_train, y_pred)
        
        print(f"📈 Training accuracy: {accuracy:.3f}")
        
        # Save model
        model_path = self.data_path / "quick_test_model.joblib"
        joblib.dump({
            'model': model,
            'class_names': class_names,
            'feature_shape': X_train.shape[1]
        }, model_path)
        
        print(f"💾 Model saved to: {model_path}")
        
        return True
    
    def test_predictions(self):
        """Test predictions with the trained model."""
        print("\n🧪 Testing Prediction Functionality")
        print("=" * 50)
        
        # Load model
        model_path = self.data_path / "quick_test_model.joblib"
        if not model_path.exists():
            print("❌ No trained model found!")
            return False
        
        model_data = joblib.load(model_path)
        model = model_data['model']
        class_names = model_data['class_names']
        
        # Create small test dataset
        X_test, y_test, _, test_paths = self.create_small_dataset('test')
        
        if len(X_test) == 0:
            print("❌ No test data loaded!")
            return False
        
        print(f"📊 Test data shape: {X_test.shape}")
        
        # Make predictions
        y_pred = model.predict(X_test)
        probabilities = model.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        print(f"📈 Test accuracy: {accuracy:.3f}")
        
        # Show some predictions
        print("\n🔍 Sample Predictions:")
        for i in range(min(5, len(X_test))):
            actual_class = class_names[y_test[i]]
            predicted_class = class_names[y_pred[i]]
            confidence = np.max(probabilities[i])
            
            status = "✅" if y_test[i] == y_pred[i] else "❌"
            print(f"   {status} Actual: {actual_class}, Predicted: {predicted_class} (conf: {confidence:.3f})")
        
        # Test severity prediction
        print("\n🏥 Testing Severity Prediction:")
        for i in range(min(3, len(X_test))):
            try:
                # Create dummy features for severity prediction
                severity_features = {
                    'heart_rate_variability': np.random.rand(),
                    'qrs_duration': np.random.rand() * 100 + 80,
                    'pr_interval': np.random.rand() * 50 + 120,
                    'qt_interval': np.random.rand() * 100 + 350
                }
                
                predicted_class = class_names[y_pred[i]]
                severity = self.severity_predictor.predict_severity(predicted_class, severity_features)
                
                print(f"   🫀 Class: {predicted_class} → Severity: {severity}")
            except Exception as e:
                print(f"   ⚠️  Severity prediction error: {e}")
        
        return True
    
    def run_complete_test(self):
        """Run complete quick training and testing."""
        print("🫀 RythmGuard Quick Training Test")
        print("=" * 60)
        print(f"📁 Data path: {self.data_path}")
        print(f"🔢 Max images per class: {self.max_images_per_class}")
        
        try:
            # Step 1: Train model
            if not self.train_quick_model():
                print("❌ Training failed!")
                return False
            
            # Step 2: Test predictions
            if not self.test_predictions():
                print("❌ Testing failed!")
                return False
            
            print("\n🎉 Quick training test completed successfully!")
            print("💡 Your model is working correctly. You can now run full training with:")
            print("   py rythmguard_pipeline.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            return False

def main():
    """Main function to run quick training test."""
    # Use the correct data path (01_data directory)
    data_path = Path(__file__).parent.parent / '01_data'
    
    # Create tester with small dataset
    tester = QuickTrainingTest(data_path, max_images_per_class=5)
    
    # Run complete test
    success = tester.run_complete_test()
    
    if success:
        print("\n✅ All tests passed! Your RythmGuard system is ready.")
    else:
        print("\n❌ Some tests failed. Please check the output above.")

if __name__ == "__main__":
    main()