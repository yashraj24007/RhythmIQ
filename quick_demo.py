"""
Quick Demo Script for RythmGuard ECG Analysis
===========================================

This script provides a quick demonstration of the RythmGuard system
without running the full pipeline.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def quick_demo():
    """
    Quick demonstration of RythmGuard capabilities
    """
    data_path = r"d:\2nd-1st Sem\AI&ML\ECG_Image_data"
    
    print("🫀 RythmGuard ECG Analysis System - Quick Demo")
    print("=" * 60)
    
    # Check if data path exists
    if not os.path.exists(data_path):
        print(f"❌ Data path not found: {data_path}")
        print("Please ensure the ECG dataset is in the correct location.")
        return
    
    # Demonstrate dataset structure analysis
    print("\n📊 Dataset Structure Analysis")
    print("-" * 40)
    
    test_path = os.path.join(data_path, 'test')
    if os.path.exists(test_path):
        class_info = {
            'N': 'Normal beats (sinus rhythm, bundle branch block, etc.)',
            'S': 'Supraventricular (Atrial premature beats, supraventricular ectopics)',
            'V': 'Ventricular (PVC - Premature Ventricular Contractions)',
            'F': 'Fusion (Fusion of ventricular + normal beat)',
            'Q': 'Unknown (Paced beats, unclassifiable beats)',
            'M': 'Myocardial Infarction (MI)'
        }
        
        total_images = 0
        for class_folder in sorted(os.listdir(test_path)):
            class_path = os.path.join(test_path, class_folder)
            if os.path.isdir(class_path):
                images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                count = len(images)
                total_images += count
                
                description = class_info.get(class_folder, 'Unknown class')
                print(f"📁 {class_folder}: {count} images - {description}")
        
        print(f"\n📈 Total test images: {total_images}")
        
        # Show sample images
        print("\n🖼️  Sample ECG Images")
        print("-" * 40)
        display_sample_images(test_path, class_info)
    
    else:
        print(f"❌ Test data not found at: {test_path}")
    
    # Demonstrate system capabilities
    print("\n🎯 RythmGuard System Capabilities")
    print("-" * 40)
    print("1. 📊 ECG Image Classification")
    print("   └─ Identifies 6 types of cardiac conditions")
    print("   └─ Uses advanced machine learning algorithms")
    print("   └─ Provides confidence scores for each prediction")
    
    print("\n2. ⚕️  Severity Level Prediction")
    print("   └─ Mild: Low-risk cases requiring routine monitoring")
    print("   └─ Moderate: Intermediate-risk cases requiring closer observation")
    print("   └─ Severe: High-risk cases requiring immediate medical attention")
    
    print("\n3. 🏥 Clinical Decision Support")
    print("   └─ Automatic priority assignment based on class and severity")
    print("   └─ Risk-based patient triage recommendations")
    print("   └─ Real-time monitoring capabilities")
    
    print("\n4. 📋 Comprehensive Analysis")
    print("   └─ Detailed performance metrics and reports")
    print("   └─ Visual analytics and confusion matrices")
    print("   └─ Dataset statistics and class distributions")
    
    # Show example workflow
    print("\n🔄 Example Workflow")
    print("-" * 40)
    print("1. Load ECG image → 📸 Image preprocessing")
    print("2. Extract features → 🔍 Feature analysis") 
    print("3. Classify condition → 🏷️  N/S/V/F/Q/M classification")
    print("4. Predict severity → ⚕️  Mild/Moderate/Severe assessment")
    print("5. Determine priority → 🚨 Clinical priority assignment")
    print("6. Generate report → 📋 Actionable insights for healthcare providers")
    
    # Next steps
    print("\n🚀 To Run Full Analysis:")
    print("-" * 40)
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Run complete pipeline: python rythmguard_pipeline.py")
    print("3. Or run individual components:")
    print("   └─ python ecg_preprocessor.py")
    print("   └─ Check outputs in rythmguard_output/ directory")
    
    print("\n✅ Demo completed! Ready to analyze your ECG data.")

def display_sample_images(test_path, class_info, max_samples=6):
    """
    Display sample images from each class
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Sample ECG Images by Classification', fontsize=16, fontweight='bold')
    
    axes = axes.ravel()
    class_folders = sorted([f for f in os.listdir(test_path) if os.path.isdir(os.path.join(test_path, f))])
    
    for i, class_folder in enumerate(class_folders[:max_samples]):
        class_path = os.path.join(test_path, class_folder)
        images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if images and i < len(axes):
            try:
                # Load first image from this class
                img_path = os.path.join(class_path, images[0])
                img = Image.open(img_path)
                
                # Display image
                axes[i].imshow(img, cmap='gray' if img.mode == 'L' else None)
                axes[i].set_title(f'{class_folder} - {class_info.get(class_folder, "Unknown").split("(")[0].strip()}', 
                                fontweight='bold')
                axes[i].axis('off')
                
            except Exception as e:
                # If image can't be loaded, show placeholder
                axes[i].text(0.5, 0.5, f'Class {class_folder}\n(Image load error)', 
                           ha='center', va='center', transform=axes[i].transAxes)
                axes[i].set_title(f'{class_folder} - Error')
                axes[i].axis('off')
    
    # Hide unused subplots
    for i in range(len(class_folders), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(test_path, '..', 'sample_ecg_preview.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"💾 Sample image preview saved to: {output_path}")
    
    plt.show()

def show_severity_mapping():
    """
    Show how severity is mapped to different ECG classes
    """
    print("\n📊 Severity Distribution by ECG Class")
    print("-" * 50)
    
    severity_rules = {
        'N': {'Mild': 80, 'Moderate': 15, 'Severe': 5},    # Normal - mostly mild
        'S': {'Mild': 60, 'Moderate': 30, 'Severe': 10},   # Supraventricular - mixed
        'V': {'Mild': 40, 'Moderate': 40, 'Severe': 20},   # Ventricular - more serious
        'F': {'Mild': 30, 'Moderate': 50, 'Severe': 20},   # Fusion - moderate to severe
        'Q': {'Mild': 50, 'Moderate': 30, 'Severe': 20},   # Unknown - uncertain
        'M': {'Mild': 10, 'Moderate': 30, 'Severe': 60}    # MI - mostly severe
    }
    
    class_names = {
        'N': 'Normal',
        'S': 'Supraventricular', 
        'V': 'Ventricular (PVC)',
        'F': 'Fusion',
        'Q': 'Unknown',
        'M': 'Myocardial Infarction'
    }
    
    for class_code, severities in severity_rules.items():
        class_name = class_names.get(class_code, 'Unknown')
        print(f"\n{class_code} - {class_name}:")
        for severity, percentage in severities.items():
            print(f"  └─ {severity}: {percentage}%")

if __name__ == "__main__":
    quick_demo()
    show_severity_mapping()