"""
RythmGuard Training Readiness Check
=================================

This script validates that everything is ready for model training.
"""

import os
import sys
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

def check_training_readiness():
    """
    Comprehensive check for training readiness
    """
    print("🔍 RythmGuard Training Readiness Check")
    print("=" * 60)
    
    readiness_score = 0
    total_checks = 8
    
    # 1. Check Python version
    print(f"\n1️⃣  Python Version: {sys.version.split()[0]}")
    if sys.version_info >= (3, 8):
        print("   ✅ Python version is compatible")
        readiness_score += 1
    else:
        print("   ❌ Python version too old (requires 3.8+)")
    
    # 2. Check essential packages
    print(f"\n2️⃣  Essential Packages:")
    required_packages = ['numpy', 'pandas', 'sklearn', 'cv2', 'matplotlib', 'PIL', 'joblib']
    packages_ok = True
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                import sklearn
                print(f"   ✅ scikit-learn: {sklearn.__version__}")
            elif package == 'cv2':
                import cv2
                print(f"   ✅ opencv-python: {cv2.__version__}")
            elif package == 'PIL':
                from PIL import Image
                print(f"   ✅ Pillow (PIL): Available")
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'Available')
                print(f"   ✅ {package}: {version}")
        except ImportError:
            print(f"   ❌ {package}: Not installed")
            packages_ok = False
    
    if packages_ok:
        readiness_score += 1
    
    # 3. Check dataset structure
    print(f"\n3️⃣  Dataset Structure:")
    data_path = "."
    
    test_path = os.path.join(data_path, 'test')
    train_path = os.path.join(data_path, 'train')
    
    if os.path.exists(test_path) and os.path.exists(train_path):
        print("   ✅ Both test and train directories exist")
        readiness_score += 1
    elif os.path.exists(test_path):
        print("   ⚠️  Only test directory exists (train split will be created)")
        readiness_score += 0.5
    else:
        print("   ❌ Dataset directories not found")
    
    # 4. Check class distribution
    print(f"\n4️⃣  Class Distribution:")
    expected_classes = ['F', 'M', 'N', 'Q', 'S', 'V']
    classes_found = 0
    
    for dataset in ['test', 'train']:
        dataset_path = os.path.join(data_path, dataset)
        if os.path.exists(dataset_path):
            print(f"   📁 {dataset.upper()} Dataset:")
            total_images = 0
            
            for class_folder in expected_classes:
                class_path = os.path.join(dataset_path, class_folder)
                if os.path.exists(class_path):
                    images = [f for f in os.listdir(class_path) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    count = len(images)
                    total_images += count
                    print(f"      {class_folder}: {count} images")
                    classes_found += 1
            
            print(f"   📊 Total {dataset} images: {total_images}")
    
    if classes_found >= 6:  # At least one full set of classes
        print("   ✅ All expected classes found")
        readiness_score += 1
    else:
        print("   ❌ Missing some expected classes")
    
    # 5. Check image accessibility
    print(f"\n5️⃣  Image Accessibility:")
    sample_images_checked = 0
    
    for dataset in ['test']:  # Check test first
        dataset_path = os.path.join(data_path, dataset)
        if os.path.exists(dataset_path):
            for class_folder in os.listdir(dataset_path):
                class_path = os.path.join(dataset_path, class_folder)
                if os.path.isdir(class_path):
                    images = [f for f in os.listdir(class_path) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if images:
                        try:
                            # Test loading first image
                            sample_path = os.path.join(class_path, images[0])
                            img = cv2.imread(sample_path)
                            if img is not None:
                                sample_images_checked += 1
                                if sample_images_checked == 1:
                                    print(f"   ✅ Sample image loaded successfully: {img.shape}")
                            break
                        except Exception as e:
                            print(f"   ❌ Error loading sample image: {e}")
                            break
            break
    
    if sample_images_checked > 0:
        readiness_score += 1
    
    # 6. Check memory availability
    print(f"\n6️⃣  System Resources:")
    try:
        # Create small test arrays to check memory
        test_array = np.random.random((1000, 224, 224, 3)).astype(np.float32)
        print(f"   ✅ Memory test passed: {test_array.nbytes / 1024 / 1024:.1f} MB allocated")
        del test_array
        readiness_score += 1
    except MemoryError:
        print("   ⚠️  Memory might be limited for large datasets")
        readiness_score += 0.5
    
    # 7. Check preprocessing capabilities
    print(f"\n7️⃣  Preprocessing Capabilities:")
    try:
        # Test basic preprocessing operations
        dummy_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        resized = cv2.resize(dummy_img, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        print("   ✅ Image preprocessing operations working")
        readiness_score += 1
    except Exception as e:
        print(f"   ❌ Preprocessing error: {e}")
    
    # 8. Check model training requirements
    print(f"\n8️⃣  Model Training Requirements:")
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score, classification_report
        
        # Test basic ML operations
        X_test = np.random.random((100, 10))
        y_test = np.random.randint(0, 6, 100)
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_test, y_test)
        predictions = model.predict(X_test)
        
        print("   ✅ Machine learning operations working")
        readiness_score += 1
    except Exception as e:
        print(f"   ❌ ML operations error: {e}")
    
    # Final readiness assessment
    print(f"\n" + "=" * 60)
    print(f"🎯 READINESS SCORE: {readiness_score}/{total_checks} ({readiness_score/total_checks*100:.1f}%)")
    
    if readiness_score >= 7:
        print("🟢 READY FOR TRAINING!")
        print("   Your model is ready to be trained. You can proceed with:")
        print("   1. Run: py rythmguard_pipeline.py")
        print("   2. Or run individual components for step-by-step training")
        return True
    elif readiness_score >= 5:
        print("🟡 MOSTLY READY")
        print("   Minor issues detected but training should work.")
        print("   Consider addressing the failed checks for optimal performance.")
        return True
    else:
        print("🔴 NOT READY")
        print("   Please resolve the critical issues before training.")
        return False

def show_next_steps():
    """Show recommended next steps"""
    print(f"\n🚀 RECOMMENDED NEXT STEPS:")
    print("-" * 40)
    print("1. 🔥 Quick Start (Recommended):")
    print("   py rythmguard_pipeline.py")
    print("   (This runs the complete pipeline)")
    
    print("\n2. 📊 Step-by-step Training:")
    print("   a) py ecg_preprocessor.py")
    print("   b) Check outputs in processed/ directory")
    print("   c) Run individual model training")
    
    print("\n3. 🧪 Custom Training:")
    print("   a) Modify parameters in the scripts")
    print("   b) Adjust class mappings if needed")
    print("   c) Customize augmentation strategies")
    
    print("\n4. 📈 After Training:")
    print("   a) Check rythmguard_output/ for results")
    print("   b) Review performance metrics")
    print("   c) Test on individual images")
    
    print(f"\n💡 TIPS:")
    print("   • Start with a small subset for testing")
    print("   • Monitor memory usage during training")
    print("   • Save checkpoints for long training sessions")
    print("   • Use the severity predictor for clinical insights")

if __name__ == "__main__":
    is_ready = check_training_readiness()
    
    if is_ready:
        show_next_steps()
    
    print(f"\n🎉 Training readiness check completed!")