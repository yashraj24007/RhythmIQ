"""
ECG Image Preprocessing Pipeline for RythmGuard
============================================

This module provides comprehensive preprocessing functionality for ECG image data
organized in the following classification system:

- N: Normal (Normal beat - sinus rhythm, bundle branch block, etc.)
- S: Supraventricular (Atrial premature beats, supraventricular ectopics)
- V: Ventricular (PVC - Premature Ventricular Contractions)
- F: Fusion (Fusion of ventricular + normal beat)
- Q: Unknown (Paced beats, unclassifiable beats)
- M: Myocardial Infarction (MI)
"""

import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class ECGPreprocessor:
    """
    ECG Image Preprocessing Class for RythmGuard System
    """
    
    def __init__(self, data_path, target_size=(224, 224)):
        """
        Initialize the ECG Preprocessor
        
        Args:
            data_path (str): Path to the dataset directory
            target_size (tuple): Target size for image resizing (height, width)
        """
        self.data_path = data_path
        self.target_size = target_size
        self.class_mapping = {
            'N': {'name': 'Normal', 'description': 'Normal beat (sinus rhythm, bundle branch block, etc.)'},
            'S': {'name': 'Supraventricular', 'description': 'Atrial premature beats, supraventricular ectopics'},
            'V': {'name': 'Ventricular', 'description': 'PVC (Premature Ventricular Contractions)'},
            'F': {'name': 'Fusion', 'description': 'Fusion of ventricular + normal beat'},
            'Q': {'name': 'Unknown', 'description': 'Paced beats, unclassifiable beats'},
            'M': {'name': 'Myocardial Infarction', 'description': 'MI - Sometimes added in extended versions'}
        }
        self.label_encoder = LabelEncoder()
        
    def analyze_dataset(self, subset='test'):
        """
        Analyze the dataset structure and class distribution
        
        Args:
            subset (str): Dataset subset ('test' or 'train')
            
        Returns:
            dict: Dataset analysis information
        """
        subset_path = os.path.join(self.data_path, subset)
        analysis = {
            'classes': {},
            'total_images': 0,
            'image_formats': set(),
            'sample_image_shapes': {}
        }
        
        print(f"📊 Analyzing {subset} dataset...")
        print("=" * 50)
        
        for class_folder in os.listdir(subset_path):
            class_path = os.path.join(subset_path, class_folder)
            if os.path.isdir(class_path):
                images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                count = len(images)
                analysis['classes'][class_folder] = count
                analysis['total_images'] += count
                
                # Get sample image info
                if images:
                    sample_img_path = os.path.join(class_path, images[0])
                    try:
                        img = cv2.imread(sample_img_path)
                        if img is not None:
                            analysis['sample_image_shapes'][class_folder] = img.shape
                            analysis['image_formats'].add(images[0].split('.')[-1].lower())
                    except Exception as e:
                        print(f"Warning: Could not read sample image from {class_folder}: {e}")
                
                class_info = self.class_mapping.get(class_folder, {'name': 'Unknown', 'description': 'Unknown class'})
                print(f"📁 {class_folder} - {class_info['name']}: {count} images")
                print(f"   └─ {class_info['description']}")
        
        print("=" * 50)
        print(f"📈 Total images: {analysis['total_images']}")
        print(f"🎯 Number of classes: {len(analysis['classes'])}")
        print(f"📷 Image formats found: {list(analysis['image_formats'])}")
        
        return analysis
    
    def load_and_preprocess_image(self, image_path, apply_augmentation=False):
        """
        Load and preprocess a single ECG image
        
        Args:
            image_path (str): Path to the image file
            apply_augmentation (bool): Whether to apply data augmentation
            
        Returns:
            numpy.ndarray: Preprocessed image array
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize image
            img = cv2.resize(img, self.target_size)
            
            # Normalize pixel values to [0, 1]
            img = img.astype(np.float32) / 255.0
            
            # Apply augmentation if requested
            if apply_augmentation:
                img = self._apply_augmentation(img)
            
            return img
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def _apply_augmentation(self, img):
        """
        Apply data augmentation techniques
        
        Args:
            img (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Augmented image
        """
        # Random brightness adjustment
        if np.random.random() > 0.5:
            brightness_factor = np.random.uniform(0.8, 1.2)
            img = np.clip(img * brightness_factor, 0, 1)
        
        # Random contrast adjustment
        if np.random.random() > 0.5:
            contrast_factor = np.random.uniform(0.8, 1.2)
            img = np.clip((img - 0.5) * contrast_factor + 0.5, 0, 1)
        
        # Random horizontal flip (might not be suitable for ECG, use carefully)
        if np.random.random() > 0.8:  # Low probability for ECG data
            img = np.fliplr(img)
        
        return img
    
    def create_dataset(self, subset='test', save_processed=True):
        """
        Create preprocessed dataset from images
        
        Args:
            subset (str): Dataset subset ('test' or 'train')
            save_processed (bool): Whether to save processed data
            
        Returns:
            tuple: (X, y, class_names) where X is images, y is labels, class_names is label mapping
        """
        subset_path = os.path.join(self.data_path, subset)
        images = []
        labels = []
        image_paths = []
        
        print(f"🔄 Processing {subset} dataset...")
        
        for class_folder in sorted(os.listdir(subset_path)):
            class_path = os.path.join(subset_path, class_folder)
            if os.path.isdir(class_path):
                class_images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                print(f"Processing class {class_folder}: {len(class_images)} images")
                
                for img_file in class_images:
                    img_path = os.path.join(class_path, img_file)
                    processed_img = self.load_and_preprocess_image(img_path)
                    
                    if processed_img is not None:
                        images.append(processed_img)
                        labels.append(class_folder)
                        image_paths.append(img_path)
        
        # Convert to numpy arrays
        X = np.array(images)
        y = np.array(labels)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        class_names = self.label_encoder.classes_
        
        print(f"✅ Dataset created successfully!")
        print(f"   📊 Shape of X: {X.shape}")
        print(f"   📊 Shape of y: {y_encoded.shape}")
        print(f"   🏷️  Classes: {list(class_names)}")
        
        # Save processed data if requested
        if save_processed:
            self._save_processed_data(X, y_encoded, class_names, subset, image_paths)
        
        return X, y_encoded, class_names, image_paths
    
    def _save_processed_data(self, X, y, class_names, subset, image_paths):
        """
        Save processed data to files
        
        Args:
            X (numpy.ndarray): Processed images
            y (numpy.ndarray): Encoded labels
            class_names (numpy.ndarray): Class names
            subset (str): Dataset subset name
            image_paths (list): List of original image paths
        """
        output_dir = os.path.join(self.data_path, 'processed')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save arrays
        np.save(os.path.join(output_dir, f'{subset}_images.npy'), X)
        np.save(os.path.join(output_dir, f'{subset}_labels.npy'), y)
        np.save(os.path.join(output_dir, f'{subset}_class_names.npy'), class_names)
        
        # Save metadata
        metadata = {
            'image_paths': image_paths,
            'original_labels': [self.label_encoder.inverse_transform([label])[0] for label in y],
            'class_mapping': self.class_mapping,
            'target_size': self.target_size,
            'total_samples': len(X)
        }
        
        pd.DataFrame(metadata).to_csv(os.path.join(output_dir, f'{subset}_metadata.csv'), index=False)
        
        print(f"💾 Processed data saved to: {output_dir}")
    
    def visualize_samples(self, X, y, class_names, num_samples=12):
        """
        Visualize sample images from each class
        
        Args:
            X (numpy.ndarray): Image data
            y (numpy.ndarray): Labels
            class_names (numpy.ndarray): Class names
            num_samples (int): Number of samples to display
        """
        fig, axes = plt.subplots(3, 4, figsize=(16, 12))
        fig.suptitle('ECG Image Samples by Class', fontsize=16, fontweight='bold')
        
        axes = axes.ravel()
        
        for i, class_name in enumerate(class_names[:num_samples]):
            # Find first image of this class
            class_indices = np.where(y == i)[0]
            if len(class_indices) > 0:
                sample_idx = class_indices[0]
                img = X[sample_idx]
                
                axes[i].imshow(img)
                axes[i].set_title(f'{class_name} - {self.class_mapping.get(class_name, {}).get("name", "Unknown")}')
                axes[i].axis('off')
            else:
                axes[i].text(0.5, 0.5, 'No samples', ha='center', va='center')
                axes[i].set_title(f'{class_name} - No Data')
                axes[i].axis('off')
        
        # Hide unused subplots
        for i in range(len(class_names), len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.data_path, 'sample_visualization.png'), dpi=300, bbox_inches='tight')
        plt.show()
    
    def get_class_distribution(self, y, class_names):
        """
        Get and visualize class distribution
        
        Args:
            y (numpy.ndarray): Labels
            class_names (numpy.ndarray): Class names
            
        Returns:
            dict: Class distribution information
        """
        unique, counts = np.unique(y, return_counts=True)
        distribution = {}
        
        print("📊 Class Distribution:")
        print("=" * 40)
        
        for i, (class_idx, count) in enumerate(zip(unique, counts)):
            class_name = class_names[class_idx]
            percentage = (count / len(y)) * 100
            distribution[class_name] = {'count': count, 'percentage': percentage}
            
            class_info = self.class_mapping.get(class_name, {'name': 'Unknown'})
            print(f"{class_name} ({class_info['name']}): {count} samples ({percentage:.1f}%)")
        
        # Create distribution plot
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.bar(range(len(unique)), counts)
        plt.xticks(range(len(unique)), [class_names[i] for i in unique])
        plt.title('Class Distribution (Count)')
        plt.ylabel('Number of Samples')
        
        plt.subplot(1, 2, 2)
        plt.pie(counts, labels=[class_names[i] for i in unique], autopct='%1.1f%%', startangle=90)
        plt.title('Class Distribution (Percentage)')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.data_path, 'class_distribution.png'), dpi=300, bbox_inches='tight')
        plt.show()
        
        return distribution

def main():
    """
    Main function to demonstrate ECG preprocessing pipeline
    """
    # Initialize preprocessor
    data_path = r"d:\2nd-1st Sem\AI&ML\ECG_Image_data"
    preprocessor = ECGPreprocessor(data_path, target_size=(224, 224))
    
    print("🫀 RythmGuard ECG Preprocessing Pipeline")
    print("=" * 50)
    
    # Analyze dataset
    analysis = preprocessor.analyze_dataset('test')
    
    # Create preprocessed dataset
    X, y, class_names, image_paths = preprocessor.create_dataset('test', save_processed=True)
    
    # Visualize samples
    preprocessor.visualize_samples(X, y, class_names)
    
    # Show class distribution
    distribution = preprocessor.get_class_distribution(y, class_names)
    
    print("\n✅ Preprocessing completed successfully!")
    print(f"📁 Processed data saved in: {os.path.join(data_path, 'processed')}")

if __name__ == "__main__":
    main()