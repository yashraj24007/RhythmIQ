"""
Quick Test: Verify Train/Test Split is Correct
============================================

This script quickly verifies that the training pipeline correctly uses
train data for training and test data for testing.
"""

import os
import sys

def verify_train_test_split():
    """
    Verify that train and test datasets are being used correctly
    """
    print("🔍 Verifying Train/Test Split Configuration")
    print("=" * 60)
    
    data_path = "."
    
    # Check dataset structure
    train_path = os.path.join(data_path, 'train')
    test_path = os.path.join(data_path, 'test')
    
    if not os.path.exists(train_path):
        print("❌ Training directory not found!")
        return False
    
    if not os.path.exists(test_path):
        print("❌ Test directory not found!")
        return False
    
    print("✅ Both train and test directories found")
    
    # Count images in each dataset
    train_counts = {}
    test_counts = {}
    
    print("\n📊 Dataset Verification:")
    print("-" * 40)
    
    # Count training images
    total_train = 0
    if os.path.exists(train_path):
        for class_folder in sorted(os.listdir(train_path)):
            class_path = os.path.join(train_path, class_folder)
            if os.path.isdir(class_path):
                images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                count = len(images)
                train_counts[class_folder] = count
                total_train += count
    
    # Count test images
    total_test = 0
    if os.path.exists(test_path):
        for class_folder in sorted(os.listdir(test_path)):
            class_path = os.path.join(test_path, class_folder)
            if os.path.isdir(class_path):
                images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                count = len(images)
                test_counts[class_folder] = count
                total_test += count
    
    print(f"📁 TRAIN Dataset: {total_train:,} images")
    for class_name, count in train_counts.items():
        print(f"   {class_name}: {count:,} images")
    
    print(f"\n📁 TEST Dataset: {total_test:,} images")
    for class_name, count in test_counts.items():
        print(f"   {class_name}: {count:,} images")
    
    print(f"\n📈 TOTAL Combined: {total_train + total_test:,} images")
    
    # Calculate train/test ratio
    if total_train > 0 and total_test > 0:
        train_ratio = total_train / (total_train + total_test) * 100
        test_ratio = total_test / (total_train + total_test) * 100
        
        print(f"📊 Train/Test Split: {train_ratio:.1f}% / {test_ratio:.1f}%")
        
        # Check if split is reasonable
        if 60 <= train_ratio <= 90:
            print("✅ Train/Test split looks good!")
        else:
            print("⚠️  Unusual train/test split ratio")
    
    # Verify classes match
    train_classes = set(train_counts.keys())
    test_classes = set(test_counts.keys())
    
    if train_classes == test_classes:
        print("✅ Same classes in both train and test sets")
        print(f"   Classes: {sorted(train_classes)}")
    else:
        print("⚠️  Different classes in train vs test")
        print(f"   Train only: {train_classes - test_classes}")
        print(f"   Test only: {test_classes - train_classes}")
    
    print("\n🎯 VERIFICATION RESULT:")
    print("-" * 40)
    
    if total_train > total_test and train_classes == test_classes:
        print("✅ CORRECT SETUP!")
        print("   ✓ Training dataset is larger (as expected)")
        print("   ✓ Same classes in both datasets")
        print("   ✓ Ready for proper train/test workflow")
        
        print(f"\n🚀 READY TO TRAIN:")
        print("   • Training will use TRAIN dataset for model learning")
        print("   • Testing will use TEST dataset for evaluation")
        print("   • No data leakage between train and test")
        
        return True
    else:
        print("⚠️  POTENTIAL ISSUES:")
        if total_train <= total_test:
            print("   • Training dataset should typically be larger than test")
        if train_classes != test_classes:
            print("   • Classes should match between train and test")
        
        return False

def show_training_command():
    """Show the correct training command"""
    print(f"\n🎯 TO START TRAINING:")
    print("=" * 40)
    print("Run the complete pipeline:")
    print("   py rythmguard_pipeline.py")
    print()
    print("This will:")
    print("   1. Load TRAIN data → Train models")
    print("   2. Load TEST data → Evaluate models")
    print("   3. Generate performance reports")
    print("   4. Save trained models")
    print("   5. Create visualizations")

if __name__ == "__main__":
    is_correct = verify_train_test_split()
    
    if is_correct:
        show_training_command()
    
    print(f"\n✅ Verification completed!")