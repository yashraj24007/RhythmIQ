"""
Advanced ECG Data Augmentation Module for RythmGuard
==================================================

This module provides specialized data augmentation techniques for ECG images
to improve model robustness and handle class imbalance.
"""

import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance, ImageFilter
import albumentations as A
from albumentations.pytorch import ToTensorV2

class ECGAugmentor:
    """
    Advanced ECG Image Augmentation Class
    """
    
    def __init__(self, severity_levels=['mild', 'moderate', 'severe']):
        """
        Initialize ECG Augmentor
        
        Args:
            severity_levels (list): List of severity levels for augmentation
        """
        self.severity_levels = severity_levels
        self.augmentation_pipeline = self._create_augmentation_pipeline()
        
    def _create_augmentation_pipeline(self):
        """
        Create augmentation pipeline using Albumentations
        
        Returns:
            albumentations.Compose: Augmentation pipeline
        """
        return A.Compose([
            A.OneOf([
                A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.7),
                A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=10, val_shift_limit=10, p=0.3),
            ], p=0.8),
            
            A.OneOf([
                A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
                A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=0.2),
                A.MultiplicativeNoise(multiplier=[0.9, 1.1], per_channel=True, p=0.2),
            ], p=0.5),
            
            A.OneOf([
                A.MotionBlur(blur_limit=3, p=0.2),
                A.MedianBlur(blur_limit=3, p=0.1),
                A.GaussianBlur(blur_limit=3, p=0.1),
            ], p=0.3),
            
            A.OneOf([
                A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50, p=0.1),
                A.GridDistortion(num_steps=5, distort_limit=0.1, p=0.1),
                A.OpticalDistortion(distort_limit=0.05, shift_limit=0.05, p=0.1),
            ], p=0.2),
            
            A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=2, p=0.3),
            
            A.RandomResizedCrop(height=224, width=224, scale=(0.9, 1.0), ratio=(0.9, 1.1), p=0.3),
            
            A.CoarseDropout(max_holes=3, max_height=8, max_width=8, min_holes=1, p=0.2),
        ])
    
    def augment_ecg_signal(self, image, severity='mild'):
        """
        Apply ECG-specific augmentation based on severity
        
        Args:
            image (numpy.ndarray): Input ECG image
            severity (str): Severity level for augmentation
            
        Returns:
            numpy.ndarray: Augmented image
        """
        # Convert to uint8 if needed
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = (image * 255).astype(np.uint8)
        
        # Apply augmentation based on severity
        if severity == 'mild':
            augmented = self._apply_mild_augmentation(image)
        elif severity == 'moderate':
            augmented = self._apply_moderate_augmentation(image)
        elif severity == 'severe':
            augmented = self._apply_severe_augmentation(image)
        else:
            augmented = image
        
        return augmented.astype(np.float32) / 255.0
    
    def _apply_mild_augmentation(self, image):
        """Apply mild augmentation for normal cases"""
        pipeline = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.05, p=0.5),
            A.GaussNoise(var_limit=(5.0, 15.0), p=0.3),
            A.ShiftScaleRotate(shift_limit=0.02, scale_limit=0.02, rotate_limit=1, p=0.3),
        ])
        return pipeline(image=image)['image']
    
    def _apply_moderate_augmentation(self, image):
        """Apply moderate augmentation for intermediate cases"""
        pipeline = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.6),
            A.GaussNoise(var_limit=(10.0, 30.0), p=0.4),
            A.MotionBlur(blur_limit=3, p=0.3),
            A.ShiftScaleRotate(shift_limit=0.03, scale_limit=0.03, rotate_limit=2, p=0.4),
            A.ElasticTransform(alpha=1, sigma=25, alpha_affine=25, p=0.2),
        ])
        return pipeline(image=image)['image']
    
    def _apply_severe_augmentation(self, image):
        """Apply severe augmentation for critical cases"""
        pipeline = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.7),
            A.OneOf([
                A.GaussNoise(var_limit=(15.0, 40.0), p=0.4),
                A.ISONoise(color_shift=(0.01, 0.03), intensity=(0.1, 0.3), p=0.3),
            ], p=0.5),
            A.OneOf([
                A.MotionBlur(blur_limit=5, p=0.3),
                A.GaussianBlur(blur_limit=3, p=0.2),
            ], p=0.4),
            A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=3, p=0.5),
            A.ElasticTransform(alpha=1, sigma=30, alpha_affine=30, p=0.3),
            A.CoarseDropout(max_holes=2, max_height=10, max_width=10, min_holes=1, p=0.3),
        ])
        return pipeline(image=image)['image']
    
    def create_synthetic_arrhythmia(self, normal_image, target_class):
        """
        Create synthetic arrhythmia patterns from normal ECG
        
        Args:
            normal_image (numpy.ndarray): Normal ECG image
            target_class (str): Target arrhythmia class
            
        Returns:
            numpy.ndarray: Synthetic arrhythmia image
        """
        if target_class == 'V':  # Ventricular (PVC)
            return self._create_pvc_pattern(normal_image)
        elif target_class == 'S':  # Supraventricular
            return self._create_sv_pattern(normal_image)
        elif target_class == 'F':  # Fusion
            return self._create_fusion_pattern(normal_image)
        elif target_class == 'M':  # Myocardial Infarction
            return self._create_mi_pattern(normal_image)
        else:
            return normal_image
    
    def _create_pvc_pattern(self, image):
        """Create PVC (Premature Ventricular Contraction) pattern"""
        # Add wider QRS complex simulation
        augmented = A.Compose([
            A.ElasticTransform(alpha=2, sigma=20, alpha_affine=20, p=0.8),
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.7),
            A.GaussNoise(var_limit=(10.0, 25.0), p=0.5),
        ])(image=image)['image']
        return augmented
    
    def _create_sv_pattern(self, image):
        """Create Supraventricular pattern"""
        # Simulate atrial premature beats
        augmented = A.Compose([
            A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.03, rotate_limit=2, p=0.7),
            A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.6),
            A.ElasticTransform(alpha=1, sigma=30, alpha_affine=15, p=0.5),
        ])(image=image)['image']
        return augmented
    
    def _create_fusion_pattern(self, image):
        """Create Fusion beat pattern"""
        # Simulate fusion of ventricular and normal beat
        augmented = A.Compose([
            A.ElasticTransform(alpha=1.5, sigma=25, alpha_affine=25, p=0.8),
            A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.6),
            A.MotionBlur(blur_limit=3, p=0.4),
            A.GaussNoise(var_limit=(5.0, 20.0), p=0.5),
        ])(image=image)['image']
        return augmented
    
    def _create_mi_pattern(self, image):
        """Create Myocardial Infarction pattern"""
        # Simulate ST elevation/depression
        augmented = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.2, p=0.8),
            A.ElasticTransform(alpha=2, sigma=15, alpha_affine=30, p=0.7),
            A.ShiftScaleRotate(shift_limit=0.03, scale_limit=0.05, rotate_limit=3, p=0.6),
            A.GaussNoise(var_limit=(15.0, 35.0), p=0.5),
        ])(image=image)['image']
        return augmented
    
    def balance_dataset(self, X, y, target_samples_per_class=None):
        """
        Balance dataset using augmentation
        
        Args:
            X (numpy.ndarray): Image data
            y (numpy.ndarray): Labels
            target_samples_per_class (int): Target number of samples per class
            
        Returns:
            tuple: Balanced (X, y)
        """
        unique_classes, class_counts = np.unique(y, return_counts=True)
        
        if target_samples_per_class is None:
            target_samples_per_class = max(class_counts)
        
        balanced_X = []
        balanced_y = []
        
        for class_idx in unique_classes:
            class_mask = y == class_idx
            class_images = X[class_mask]
            class_labels = y[class_mask]
            
            current_count = len(class_images)
            needed_samples = target_samples_per_class - current_count
            
            # Add original images
            balanced_X.extend(class_images)
            balanced_y.extend(class_labels)
            
            # Generate augmented samples if needed
            if needed_samples > 0:
                print(f"Generating {needed_samples} augmented samples for class {class_idx}")
                
                for i in range(needed_samples):
                    # Select random image from this class
                    random_idx = np.random.randint(0, current_count)
                    original_image = class_images[random_idx]
                    
                    # Apply random severity augmentation
                    severity = np.random.choice(self.severity_levels)
                    augmented_image = self.augment_ecg_signal(original_image, severity)
                    
                    balanced_X.append(augmented_image)
                    balanced_y.append(class_idx)
        
        return np.array(balanced_X), np.array(balanced_y)