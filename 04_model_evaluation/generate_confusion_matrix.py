#!/usr/bin/env python3
"""
🫀 Enhanced Confusion Matrix Generator
====================================
Generate a beautifully formatted confusion matrix for the ECG classification model.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import confusion_matrix, classification_report
from pathlib import Path

# Add paths for custom modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '02_preprocessing'))

def generate_enhanced_confusion_matrix():
    """Generate an enhanced confusion matrix visualization."""
    
    print("🎨 Enhanced Confusion Matrix Generator")
    print("=" * 60)
    
    # Check if model exists
    data_path = Path("01_data")
    model_path = data_path / "rythmguard_model.joblib"
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return False
    
    # Load model
    print("📁 Loading trained model...")
    model_data = joblib.load(model_path)
    model = model_data['model']
    class_names = model_data['class_names']
    
    print(f"✅ Model loaded successfully")
    print(f"🎯 Classes: {class_names}")
    
    # Load test results if available
    try:
        # Try to use existing test data or load from full test evaluation results
        from ecg_preprocessor import ECGPreprocessor
        preprocessor = ECGPreprocessor(str(data_path), target_size=(224, 224))
        
        # Quick test with small dataset for demo
        print("🔄 Generating test data for confusion matrix...")
        test_images = []
        test_labels = []
        
        test_path = data_path / 'test'
        for class_idx, class_name in enumerate(class_names):
            class_folder = test_path / class_name
            if class_folder.exists():
                images = list(class_folder.glob("*.png"))[:20]  # 20 images per class for demo
                for img_path in images:
                    processed_img = preprocessor.load_and_preprocess_image(str(img_path))
                    if processed_img is not None:
                        test_images.append(processed_img)
                        test_labels.append(class_idx)
        
        X_test = np.array(test_images)
        # Flatten images for RandomForest (expects 2D)
        X_test = X_test.reshape(X_test.shape[0], -1)
        y_test = np.array(test_labels)
        
        # Make predictions
        print("🔍 Making predictions...")
        y_pred = model.predict(X_test)
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Create enhanced visualization
        plt.style.use('default')
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Standard confusion matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names,
                   ax=axes[0])
        axes[0].set_title('🫀 ECG Classification Confusion Matrix\n(Absolute Values)', 
                         fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Predicted Class', fontsize=12)
        axes[0].set_ylabel('True Class', fontsize=12)
        
        # Plot 2: Normalized confusion matrix
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='RdYlBu_r',
                   xticklabels=class_names, yticklabels=class_names,
                   ax=axes[1], vmin=0, vmax=1)
        axes[1].set_title('🫀 ECG Classification Confusion Matrix\n(Normalized)', 
                         fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Predicted Class', fontsize=12)
        axes[1].set_ylabel('True Class', fontsize=12)
        
        # Add class descriptions
        class_descriptions = {
            'F': 'Fusion beats',
            'M': 'Myocardial Infarction', 
            'N': 'Normal beats',
            'Q': 'Unknown beats',
            'S': 'Supraventricular',
            'V': 'Ventricular (PVC)'
        }
        
        # Add legend
        legend_text = "Class Descriptions:\n"
        for cls, desc in class_descriptions.items():
            if cls in class_names:
                legend_text += f"{cls}: {desc}\n"
        
        fig.text(0.02, 0.02, legend_text, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.tight_layout()
        
        # Save the enhanced confusion matrix
        output_path = Path("07_results_visualizations") / "enhanced_confusion_matrix.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ Enhanced confusion matrix saved: {output_path}")
        
        # Print classification report
        print("\n📊 Classification Report:")
        print("=" * 50)
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Calculate accuracy
        accuracy = np.mean(y_pred == y_test)
        print(f"\n🎯 Overall Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Could not generate enhanced confusion matrix: {e}")
        return False

if __name__ == "__main__":
    success = generate_enhanced_confusion_matrix()
    
    if success:
        print("\n✅ Enhanced confusion matrix generation completed!")
        print("📁 Check '07_results_visualizations/enhanced_confusion_matrix.png'")
    else:
        print("\n❌ Enhanced confusion matrix generation failed.")
