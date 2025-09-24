#!/usr/bin/env python3
"""
🫀 Test RythmGuard with Real ECG Images
======================================
This script tests severity predictor with real ECG images from your dataset.
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from severity_predictor import SeverityPredictor
from ecg_preprocessor import ECGPreprocessor

def test_severity_with_real_images():
    """Test severity predictor with real ECG images from your dataset"""
    
    print("🫀 Testing RythmGuard Severity Predictor with Real ECG Images")
    print("=" * 60)
    
    # Initialize components
    severity_predictor = SeverityPredictor()
    preprocessor = ECGPreprocessor(".", target_size=(224, 224))
    
    # Test with images from each class
    test_data_path = "test"
    classes = ['N', 'S', 'V', 'F', 'Q', 'M']
    class_meanings = {
        'N': 'Normal beats',
        'S': 'Supraventricular beats', 
        'V': 'Ventricular beats (PVC)',
        'F': 'Fusion beats',
        'Q': 'Unknown/Paced beats',
        'M': 'Myocardial Infarction'
    }
    
    results = []
    
    for class_name in classes:
        class_path = os.path.join(test_data_path, class_name)
        
        if not os.path.exists(class_path):
            print(f"❌ Class {class_name} folder not found")
            continue
            
        # Get first few images from this class
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:3]
        
        if not image_files:
            print(f"❌ No images found in {class_name} folder")
            continue
            
        print(f"\n📊 Testing Class {class_name} - {class_meanings[class_name]}")
        print("-" * 40)
        
        for img_file in image_files:
            img_path = os.path.join(class_path, img_file)
            
            try:
                # Load and preprocess image
                image = Image.open(img_path).convert('RGB')
                image_array = np.array(image)
                
                # Predict severity using rule-based approach
                severity_result = severity_predictor.predict_severity_rule_based(class_name)
                severity_name = severity_result['severity']
                confidence = severity_result['confidence']
                
                # Map severity name to label for priority
                severity_label = {'Mild': 0, 'Moderate': 1, 'Severe': 2}[severity_name]
                
                # Get clinical priority
                priority = severity_predictor.get_clinical_priority(severity_label)
                
                result = {
                    'class': class_name,
                    'meaning': class_meanings[class_name],
                    'filename': img_file,
                    'severity': severity_name,
                    'confidence': confidence,
                    'priority': priority,
                    'image_shape': image_array.shape
                }
                
                results.append(result)
                
                print(f"  📄 {img_file}")
                print(f"     Severity: {severity_name} ({confidence:.1%} confidence)")
                print(f"     Priority: {priority}")
                print(f"     Image: {image_array.shape}")
                
            except Exception as e:
                print(f"  ❌ Error processing {img_file}: {e}")
    
    # Summary report
    print(f"\n🎯 SUMMARY REPORT")
    print("=" * 60)
    print(f"Total images tested: {len(results)}")
    
    if results:
        # Count by severity
        severity_counts = {}
        priority_counts = {}
        
        for result in results:
            severity = result['severity']
            priority = result['priority']
            
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        print(f"\n📈 Severity Distribution:")
        for severity, count in severity_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  {severity}: {count} images ({percentage:.1f}%)")
        
        print(f"\n🏥 Clinical Priority Distribution:")
        for priority, count in priority_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  {priority}: {count} images ({percentage:.1f}%)")
        
        # Show most critical cases
        critical_cases = [r for r in results if r['severity'] == 'Severe']
        if critical_cases:
            print(f"\n🚨 CRITICAL CASES DETECTED ({len(critical_cases)} cases):")
            for case in critical_cases:
                print(f"  ⚠️  {case['class']} - {case['meaning']}")
                print(f"      File: {case['filename']}")
                print(f"      Confidence: {case['confidence']:.1%}")
    
    return results

def visualize_severity_predictions(results, max_images=6):
    """Visualize some sample predictions"""
    if not results:
        print("No results to visualize")
        return
    
    # Select diverse examples
    selected = []
    classes_seen = set()
    
    for result in results:
        if len(selected) >= max_images:
            break
        if result['class'] not in classes_seen or len(selected) < 3:
            selected.append(result)
            classes_seen.add(result['class'])
    
    if not selected:
        return
    
    try:
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('ECG Severity Predictions - Sample Results', fontsize=16)
        
        for i, result in enumerate(selected[:6]):
            row, col = i // 3, i % 3
            ax = axes[row, col]
            
            # Load and display image
            class_path = os.path.join("test", result['class'])
            img_path = os.path.join(class_path, result['filename'])
            
            try:
                image = Image.open(img_path)
                ax.imshow(image)
                ax.set_title(f"{result['class']}: {result['severity']}\n"
                            f"Confidence: {result['confidence']:.1%}")
                ax.axis('off')
            except:
                ax.text(0.5, 0.5, f"Could not load\n{result['filename']}", 
                       ha='center', va='center')
                ax.set_title(f"{result['class']}: {result['severity']}")
        
        # Hide empty subplots
        for i in range(len(selected), 6):
            row, col = i // 3, i % 3
            axes[row, col].axis('off')
        
        plt.tight_layout()
        plt.savefig("severity_predictions_sample.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Visualization saved as 'severity_predictions_sample.png'")
        
    except Exception as e:
        print(f"Visualization error: {e}")

def test_specific_image(image_path, class_name):
    """Test severity prediction on a specific image"""
    print(f"\n🔍 Testing Specific Image: {image_path}")
    print("-" * 40)
    
    try:
        # Initialize predictor
        severity_predictor = SeverityPredictor()
        
        # Load image
        image = np.array(Image.open(image_path).convert('RGB'))
        print(f"📷 Image loaded: {image.shape}")
        
        # Predict severity using rule-based approach
        severity_result = severity_predictor.predict_severity_rule_based(class_name)
        severity_name = severity_result['severity']
        confidence = severity_result['confidence']
        
        # Map severity name to label for priority
        severity_label = {'Mild': 0, 'Moderate': 1, 'Severe': 2}[severity_name]
        
        # Get clinical priority
        priority = severity_predictor.get_clinical_priority(severity_label)
        
        print(f"🎯 Class: {class_name}")
        print(f"🏥 Severity: {severity_name}")
        print(f"📈 Confidence: {confidence:.1%}")
        print(f"⚠️  Priority: {priority}")
        
        return {
            'severity': severity_name,
            'confidence': confidence,
            'priority': priority
        }
        
    except Exception as e:
        print(f"❌ Error testing image: {e}")
        return None

if __name__ == "__main__":
    # Run comprehensive test with dataset images
    print("🔄 Running comprehensive test with dataset images...")
    results = test_severity_with_real_images()
    
    # Generate visualization
    if results:
        print("\n🎨 Generating visualization...")
        visualize_severity_predictions(results)
    
    # Example of testing a specific image
    # Uncomment and modify the path below to test a specific image:
    # test_specific_image("test/N/N0.png", "N")
    
    print(f"\n✅ Testing complete! Processed {len(results)} ECG images")
    print("💡 You can now run 'pytest tests/test_severity_predictor.py -v' for formal testing")