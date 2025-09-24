#!/usr/bin/env python3
"""
🫀 Full Test Dataset Evaluation
==============================
This script evaluates the trained model on the COMPLETE test dataset.
"""

import os
import numpy as np
import joblib
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from ecg_preprocessor import ECGPreprocessor
import time

def evaluate_full_test_dataset(max_images_per_class=None):
    """Evaluate model on the complete test dataset"""
    
    print("🧪 Full Test Dataset Evaluation")
    print("=" * 60)
    
    # Check if model exists
    model_path = "rythmguard_model.joblib"
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False
    
    # Load model
    print("📁 Loading trained model...")
    model_data = joblib.load(model_path)
    model = model_data['model']
    class_names = model_data['class_names']
    
    print(f"✅ Model loaded successfully")
    print(f"🎯 Classes: {class_names}")
    
    # Initialize preprocessor
    preprocessor = ECGPreprocessor(".", target_size=(224, 224))
    
    # Collect all test data
    print(f"\n🔄 Loading Full Test Dataset")
    print("-" * 40)
    
    all_images = []
    all_labels = []
    all_predictions = []
    all_probabilities = []
    class_counts = {}
    
    total_start_time = time.time()
    
    for class_idx, class_name in enumerate(class_names):
        class_path = os.path.join("test", class_name)
        
        if not os.path.exists(class_path):
            print(f"⚠️ Test folder not found: {class_path}")
            continue
        
        # Get all test images for this class
        image_files = [f for f in os.listdir(class_path) if f.lower().endswith('.png')]
        
        # Limit if specified
        if max_images_per_class and len(image_files) > max_images_per_class:
            image_files = image_files[:max_images_per_class]
        
        class_counts[class_name] = len(image_files)
        print(f"📁 {class_name}: Processing {len(image_files)} images...")
        
        class_start_time = time.time()
        processed_count = 0
        
        for img_file in image_files:
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
                
                all_images.append(img_path)
                all_labels.append(class_idx)
                all_predictions.append(prediction)
                all_probabilities.append(probabilities)
                
                processed_count += 1
                
                # Progress indicator
                if processed_count % 50 == 0:
                    print(f"   ⏳ Processed {processed_count}/{len(image_files)}")
                
            except Exception as e:
                print(f"   ❌ Error processing {img_file}: {e}")
                continue
        
        class_time = time.time() - class_start_time
        print(f"   ✅ {class_name}: {processed_count} images processed in {class_time:.1f}s")
    
    total_time = time.time() - total_start_time
    
    # Calculate results
    print(f"\n📊 FULL TEST DATASET RESULTS")
    print("=" * 60)
    
    if not all_labels:
        print("❌ No test data processed!")
        return False
    
    # Overall accuracy
    accuracy = accuracy_score(all_labels, all_predictions)
    total_images = len(all_labels)
    
    print(f"📈 Total test images: {total_images}")
    print(f"🎯 Overall accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    print(f"⏱️ Total processing time: {total_time:.1f} seconds")
    print(f"📊 Average time per image: {total_time/total_images:.3f} seconds")
    
    # Detailed classification report
    print(f"\n📋 Detailed Classification Report:")
    print("=" * 50)
    report = classification_report(all_labels, all_predictions, target_names=class_names, digits=3)
    print(report)
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_predictions)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=class_names, yticklabels=class_names)
    plt.title(f'Full Test Dataset Confusion Matrix\n(Total Images: {total_images})')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('full_test_confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Full confusion matrix saved: full_test_confusion_matrix.png")
    
    # Per-class performance
    print(f"\n📈 Performance by Class:")
    print("-" * 30)
    for i, class_name in enumerate(class_names):
        class_mask = np.array(all_labels) == i
        class_predictions = np.array(all_predictions)[class_mask]
        class_labels = np.array(all_labels)[class_mask]
        
        if len(class_labels) > 0:
            class_accuracy = accuracy_score(class_labels, class_predictions)
            print(f"  {class_name}: {class_accuracy:.3f} ({np.sum(class_predictions == i)}/{len(class_labels)} correct)")
    
    # Confidence analysis
    all_confidences = [np.max(probs) for probs in all_probabilities]
    avg_confidence = np.mean(all_confidences)
    min_confidence = np.min(all_confidences)
    max_confidence = np.max(all_confidences)
    
    print(f"\n🔍 Confidence Analysis:")
    print("-" * 25)
    print(f"  Average confidence: {avg_confidence:.3f}")
    print(f"  Min confidence: {min_confidence:.3f}")
    print(f"  Max confidence: {max_confidence:.3f}")
    
    # Low confidence predictions
    low_conf_threshold = 0.6
    low_conf_count = sum(1 for conf in all_confidences if conf < low_conf_threshold)
    print(f"  Low confidence (<{low_conf_threshold}): {low_conf_count} images ({low_conf_count/total_images*100:.1f}%)")
    
    # Error analysis
    incorrect_mask = np.array(all_labels) != np.array(all_predictions)
    incorrect_count = np.sum(incorrect_mask)
    
    if incorrect_count > 0:
        print(f"\n❌ Error Analysis ({incorrect_count} errors):")
        print("-" * 30)
        
        error_classes = {}
        for i, (true_label, pred_label, conf) in enumerate(zip(
            np.array(all_labels)[incorrect_mask],
            np.array(all_predictions)[incorrect_mask], 
            np.array(all_confidences)[incorrect_mask]
        )):
            true_class = class_names[true_label]
            pred_class = class_names[pred_label]
            error_key = f"{true_class} → {pred_class}"
            
            if error_key not in error_classes:
                error_classes[error_key] = []
            error_classes[error_key].append(conf)
        
        for error_type, confidences in error_classes.items():
            avg_conf = np.mean(confidences)
            print(f"  {error_type}: {len(confidences)} errors (avg conf: {avg_conf:.3f})")
    
    print(f"\n🎉 Full test evaluation completed!")
    print(f"📊 Model achieves {accuracy:.1%} accuracy on {total_images} test images")
    
    return True

def quick_sample_test(sample_size=100):
    """Quick test on a random sample"""
    print(f"🚀 Quick Sample Test ({sample_size} images per class)")
    return evaluate_full_test_dataset(max_images_per_class=sample_size)

if __name__ == "__main__":
    print("🫀 RythmGuard Full Test Evaluation")
    print("=" * 50)
    print("Choose evaluation mode:")
    print("1. Quick sample (100 images per class) - ~2 minutes")
    print("2. Medium sample (500 images per class) - ~10 minutes") 
    print("3. Large sample (1000 images per class) - ~20 minutes")
    print("4. Full test dataset (all 24,799 images) - ~60 minutes")
    
    try:
        choice = input("\nEnter your choice (1-4) [default: 1]: ").strip()
        if not choice:
            choice = "1"
        
        if choice == "1":
            success = quick_sample_test(100)
        elif choice == "2":
            success = evaluate_full_test_dataset(500)
        elif choice == "3":
            success = evaluate_full_test_dataset(1000)
        elif choice == "4":
            success = evaluate_full_test_dataset()
        else:
            print("Invalid choice, running quick sample...")
            success = quick_sample_test(100)
        
        if success:
            print("\n✅ Evaluation completed successfully!")
        else:
            print("\n❌ Evaluation failed!")
            
    except KeyboardInterrupt:
        print("\n👋 Evaluation cancelled by user.")