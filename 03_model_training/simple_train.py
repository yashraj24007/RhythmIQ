#!/usr/bin/env python3
"""
🫀 RythmGuard Simple Training
============================
A simplified training script that processes data in manageable chunks.
"""

import os
import sys
import time
import random
from pathlib import Path
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Add current directory and preprocessing directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '02_preprocessing'))

from ecg_preprocessor import ECGPreprocessor
from severity_predictor import SeverityPredictor

class SimpleTrainer:
    def __init__(self, data_path, images_per_class=100):
        """Initialize simple trainer."""
        self.data_path = Path(data_path)
        self.images_per_class = images_per_class
        self.preprocessor = ECGPreprocessor(data_path)
        self.severity_predictor = SeverityPredictor()
        
    def load_balanced_dataset(self, split='train'):
        """Load a balanced dataset with specified number of images per class."""
        print(f"🔄 Loading {split} dataset ({self.images_per_class} images per class)")
        
        split_path = self.data_path / split
        if not split_path.exists():
            raise FileNotFoundError(f"Dataset split not found: {split_path}")
        
        X, y, class_names, image_paths = [], [], [], []
        
        # Get class folders
        class_folders = [f for f in split_path.iterdir() if f.is_dir()]
        class_folders.sort()
        
        for class_idx, class_folder in enumerate(class_folders):
            class_name = class_folder.name
            if class_idx == 0:  # Only add class names once
                class_names.append(class_name)
            
            # Get random sample of images from this class
            image_files = list(class_folder.glob("*.png"))
            if len(image_files) > self.images_per_class:
                image_files = random.sample(image_files, self.images_per_class)
            
            print(f"   📁 {class_name}: {len(image_files)} images")
            
            processed_count = 0
            for img_path in image_files:
                try:
                    # Load and preprocess image
                    processed_img = self.preprocessor.load_and_preprocess_image(str(img_path))
                    if processed_img is not None:
                        # Flatten image for traditional ML
                        X.append(processed_img.flatten())
                        y.append(class_idx)
                        image_paths.append(str(img_path))
                        processed_count += 1
                    
                    # Progress indicator
                    if processed_count % 10 == 0:
                        print(f"      ⏳ Processed {processed_count}/{len(image_files)}")
                        
                except Exception as e:
                    print(f"   ⚠️  Error processing {img_path.name}: {e}")
                    continue
        
        # Fix class_names to include all classes
        if len(class_names) == 1:
            class_names = [f.name for f in class_folders]
        
        return np.array(X), np.array(y), class_names, image_paths
    
    def train_model(self):
        """Train the ECG classification model."""
        print("\n🚀 Training ECG Classification Model")
        print("=" * 60)
        
        # Load training data
        X_train, y_train, class_names, train_paths = self.load_balanced_dataset('train')
        
        if len(X_train) == 0:
            print("❌ No training data loaded!")
            return None, None
        
        print(f"📊 Training data shape: {X_train.shape}")
        print(f"🎯 Classes: {class_names}")
        print(f"📈 Samples per class: ~{len(X_train) // len(class_names)}")
        
        # Train model
        print("🔄 Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=50,   # Moderate number for balance of speed/accuracy
            max_depth=10,      # Reasonable depth
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        print(f"✅ Model trained in {training_time:.2f} seconds")
        
        # Evaluate on training data
        y_pred_train = model.predict(X_train)
        train_accuracy = accuracy_score(y_train, y_pred_train)
        print(f"📈 Training accuracy: {train_accuracy:.3f}")
        
        # Save model
        model_path = self.data_path / "rythmguard_model.joblib"
        joblib.dump({
            'model': model,
            'class_names': class_names,
            'feature_shape': X_train.shape[1],
            'training_accuracy': train_accuracy,
            'training_time': training_time,
            'images_per_class': self.images_per_class
        }, model_path)
        
        print(f"💾 Model saved to: {model_path}")
        
        return model, class_names
    
    def evaluate_model(self):
        """Evaluate the trained model on test data."""
        print("\n🧪 Evaluating Model on Test Data")
        print("=" * 60)
        
        # Load model
        model_path = self.data_path / "rythmguard_model.joblib"
        if not model_path.exists():
            print("❌ No trained model found! Run training first.")
            return False
        
        model_data = joblib.load(model_path)
        model = model_data['model']
        class_names = model_data['class_names']
        
        print(f"📁 Loaded model trained with {model_data.get('images_per_class', 'unknown')} images per class")
        
        # Load test data
        X_test, y_test, _, test_paths = self.load_balanced_dataset('test')
        
        if len(X_test) == 0:
            print("❌ No test data loaded!")
            return False
        
        print(f"📊 Test data shape: {X_test.shape}")
        
        # Make predictions
        print("🔄 Making predictions...")
        y_pred = model.predict(X_test)
        probabilities = model.predict_proba(X_test)
        
        # Calculate metrics
        test_accuracy = accuracy_score(y_test, y_pred)
        print(f"📈 Test accuracy: {test_accuracy:.3f}")
        
        # Detailed classification report
        print("\n📊 Detailed Classification Report:")
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Show confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(self.data_path / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("📊 Confusion matrix saved to: confusion_matrix.png")
        
        # Show sample predictions
        print("\n🔍 Sample Predictions:")
        for i in range(min(10, len(X_test))):
            actual_class = class_names[y_test[i]]
            predicted_class = class_names[y_pred[i]]
            confidence = np.max(probabilities[i])
            
            status = "✅" if y_test[i] == y_pred[i] else "❌"
            print(f"   {status} Actual: {actual_class}, Predicted: {predicted_class} (conf: {confidence:.3f})")
        
        return True
    
    def run_complete_training(self):
        """Run complete training and evaluation."""
        print("🫀 RythmGuard Simple Training")
        print("=" * 60)
        print(f"📁 Data path: {self.data_path}")
        print(f"🔢 Images per class: {self.images_per_class}")
        
        try:
            # Step 1: Train model
            model, class_names = self.train_model()
            if model is None:
                print("❌ Training failed!")
                return False
            
            # Step 2: Evaluate model
            if not self.evaluate_model():
                print("❌ Evaluation failed!")
                return False
            
            print("\n🎉 Training completed successfully!")
            print("💡 Your trained model is ready for use.")
            print("📁 Model saved as: rythmguard_model.joblib")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during training: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function to run simple training."""
    # Use the correct data path (01_data directory)
    data_path = Path(__file__).parent.parent / '01_data'
    
    # Get user preference for dataset size
    print("🫀 RythmGuard Simple Training Setup")
    print("=" * 40)
    print("Choose training dataset size:")
    print("1. All available data (50 images per class) - ~5 minutes")
    print("2. Small dataset (20 images per class) - ~2 minutes") 
    print("3. Medium dataset (35 images per class) - ~3 minutes")
    print("4. Large dataset (50 images per class) - ~5 minutes")
    
    try:
        choice = input("\nEnter your choice (1-4) [default: 1]: ").strip()
        if not choice:
            choice = "1"
        
        size_map = {
            "1": 50,
            "2": 20, 
            "3": 35,
            "4": 50
        }
        
        images_per_class = size_map.get(choice, 50)
        
    except KeyboardInterrupt:
        print("\n👋 Training cancelled by user.")
        return
    
    # Create trainer
    trainer = SimpleTrainer(data_path, images_per_class=images_per_class)
    
    # Run training
    success = trainer.run_complete_training()
    
    if success:
        print("\n✅ Training completed! Your RythmGuard model is ready.")
        print("🧪 Run 'py test_model.py' to test your trained model.")
    else:
        print("\n❌ Training failed. Please check the output above.")

if __name__ == "__main__":
    main()