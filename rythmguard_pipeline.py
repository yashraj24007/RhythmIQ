"""
Complete RythmGuard Pipeline
==========================

This script combines ECG preprocessing, classification, and severity prediction
into a complete pipeline for the RythmGuard system.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from ecg_preprocessor import ECGPreprocessor
from severity_predictor import SeverityPredictor

class RythmGuardPipeline:
    """
    Complete RythmGuard ECG Analysis Pipeline
    """
    
    def __init__(self, data_path, target_size=(224, 224)):
        """
        Initialize RythmGuard Pipeline
        
        Args:
            data_path (str): Path to ECG dataset
            target_size (tuple): Target image size
        """
        self.data_path = data_path
        self.target_size = target_size
        self.preprocessor = ECGPreprocessor(data_path, target_size)
        self.severity_predictor = SeverityPredictor()
        self.classification_model = None
        
        # Create output directories
        self.output_dir = os.path.join(data_path, 'rythmguard_output')
        self.models_dir = os.path.join(self.output_dir, 'models')
        self.reports_dir = os.path.join(self.output_dir, 'reports')
        self.visualizations_dir = os.path.join(self.output_dir, 'visualizations')
        
        for dir_path in [self.output_dir, self.models_dir, self.reports_dir, self.visualizations_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def run_complete_pipeline(self):
        """
        Run the complete RythmGuard pipeline
        """
        print("🫀 RythmGuard Complete Pipeline")
        print("=" * 60)
        
        # Step 1: Analyze and preprocess training data
        print("\n📊 Step 1: Training Data Analysis and Preprocessing")
        print("-" * 50)
        train_analysis = self.preprocessor.analyze_dataset('train')
        X_train, y_train, class_names, train_image_paths = self.preprocessor.create_dataset('train', save_processed=True)
        
        # Step 2: Preprocess test data
        print("\n📊 Step 2: Test Data Preprocessing")
        print("-" * 50)
        test_analysis = self.preprocessor.analyze_dataset('test')
        X_test, y_test, _, test_image_paths = self.preprocessor.create_dataset('test', save_processed=True)
        
        # Step 3: Train classification model
        print("\n🤖 Step 3: Training ECG Classification Model")
        print("-" * 50)
        self._train_classification_model(X_train, y_train, class_names)
        
        # Step 4: Evaluate classification
        print("\n📈 Step 4: Classification Evaluation")
        print("-" * 50)
        classification_results = self._evaluate_classification(X_test, y_test, class_names)
        
        # Step 5: Train severity prediction
        print("\n⚕️  Step 5: Training Severity Prediction Model")
        print("-" * 50)
        severity_results = self._train_severity_prediction(X_train, y_train, class_names)
        
        # Step 6: Complete evaluation
        print("\n🔍 Step 6: Complete System Evaluation")
        print("-" * 50)
        complete_results = self._evaluate_complete_system(X_test, y_test, class_names)
        
        # Step 7: Generate comprehensive report
        print("\n📋 Step 7: Generating Comprehensive Report")
        print("-" * 50)
        self._generate_comprehensive_report(train_analysis, test_analysis, classification_results, 
                                          severity_results, complete_results, class_names)
        
        print(f"\n✅ Pipeline completed successfully!")
        print(f"📁 All outputs saved to: {self.output_dir}")
        
        return {
            'test_analysis': test_analysis,
            'classification_results': classification_results,
            'severity_results': severity_results,
            'complete_results': complete_results
        }
    
    def _train_classification_model(self, X_train, y_train, class_names):
        """Train ECG classification model"""
        # Flatten images for traditional ML model
        X_train_flat = X_train.reshape(X_train.shape[0], -1)
        
        # Train Random Forest classifier
        self.classification_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=20,
            min_samples_split=5,
            n_jobs=-1
        )
        
        print("Training classification model...")
        self.classification_model.fit(X_train_flat, y_train)
        
        # Save model
        model_path = os.path.join(self.models_dir, 'ecg_classification_model.joblib')
        joblib.dump(self.classification_model, model_path)
        print(f"Classification model saved to: {model_path}")
    
    def _evaluate_classification(self, X_test, y_test, class_names):
        """Evaluate classification model"""
        X_test_flat = X_test.reshape(X_test.shape[0], -1)
        
        # Predictions
        y_pred = self.classification_model.predict(X_test_flat)
        y_pred_proba = self.classification_model.predict_proba(X_test_flat)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        classification_rep = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        print(f"Classification Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Visualize confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                    xticklabels=class_names, yticklabels=class_names)
        plt.title('ECG Classification Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, 'classification_confusion_matrix.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'accuracy': accuracy,
            'classification_report': classification_rep,
            'confusion_matrix': conf_matrix,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
    
    def _train_severity_prediction(self, X_train, y_train, class_names):
        """Train severity prediction model"""
        print("Extracting features for severity prediction...")
        
        # Extract features for each training sample
        X_features = []
        for i, (image, class_idx) in enumerate(zip(X_train, y_train)):
            if i % 100 == 0:
                print(f"Processing image {i+1}/{len(X_train)}")
            
            ecg_class = class_names[class_idx]
            features = self.severity_predictor.extract_severity_features(image, ecg_class)
            X_features.append(features)
        
        X_features = np.array(X_features)
        
        # Generate severity labels based on ECG classes
        ecg_classes = [class_names[idx] for idx in y_train]
        y_severity = self.severity_predictor.generate_severity_labels(ecg_classes)
        
        # Train severity model
        self.severity_predictor.train_severity_model(X_features, y_severity)
        
        # Save severity model
        severity_model_path = os.path.join(self.models_dir, 'severity_prediction_model.joblib')
        self.severity_predictor.save_model(severity_model_path)
        
        return {
            'features_shape': X_features.shape,
            'severity_distribution': np.bincount(y_severity),
            'model_path': severity_model_path
        }
    
    def _evaluate_complete_system(self, X_test, y_test, class_names):
        """Evaluate complete RythmGuard system"""
        results = []
        
        print("Evaluating complete system on test data...")
        
        for i, (image, true_class_idx) in enumerate(zip(X_test, y_test)):
            if i % 50 == 0:
                print(f"Processing test image {i+1}/{len(X_test)}")
            
            # Classification prediction
            image_flat = image.reshape(1, -1)
            pred_class_idx = self.classification_model.predict(image_flat)[0]
            class_confidence = np.max(self.classification_model.predict_proba(image_flat))
            
            # Severity prediction
            pred_class = class_names[pred_class_idx]
            severity_label, severity_confidence, severity_name = self.severity_predictor.predict_severity(
                image, pred_class
            )
            
            results.append({
                'image_index': i,
                'true_class': class_names[true_class_idx],
                'predicted_class': pred_class,
                'classification_confidence': class_confidence,
                'predicted_severity': severity_name,
                'severity_confidence': severity_confidence,
                'classification_correct': true_class_idx == pred_class_idx
            })
        
        # Convert to DataFrame for analysis
        results_df = pd.DataFrame(results)
        
        # Calculate system metrics
        classification_accuracy = results_df['classification_correct'].mean()
        
        # Severity distribution by class
        severity_by_class = results_df.groupby('predicted_class')['predicted_severity'].value_counts().unstack(fill_value=0)
        
        print(f"\n🎯 Complete System Performance:")
        print(f"Classification Accuracy: {classification_accuracy:.3f}")
        print(f"\nSeverity Distribution by Class:")
        print(severity_by_class)
        
        # Visualize severity distribution
        plt.figure(figsize=(12, 8))
        severity_by_class.plot(kind='bar', stacked=True, figsize=(12, 6))
        plt.title('Severity Distribution by ECG Class')
        plt.xlabel('ECG Class')
        plt.ylabel('Number of Cases')
        plt.xticks(rotation=45)
        plt.legend(title='Severity Level')
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, 'severity_distribution.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save results
        results_df.to_csv(os.path.join(self.reports_dir, 'complete_system_results.csv'), index=False)
        
        return {
            'results_df': results_df,
            'classification_accuracy': classification_accuracy,
            'severity_distribution': severity_by_class
        }
    
    def _generate_comprehensive_report(self, train_analysis, test_analysis, classification_results, 
                                     severity_results, complete_results, class_names):
        """Generate comprehensive analysis report"""
        report_path = os.path.join(self.reports_dir, 'rythmguard_comprehensive_report.md')
        
        with open(report_path, 'w') as f:
            f.write("# RythmGuard ECG Analysis System - Comprehensive Report\n\n")
            f.write("## System Overview\n")
            f.write("RythmGuard is an AI-powered ECG monitoring system designed to analyze heart signals in real time.\n")
            f.write("It processes ECG images, detects irregularities, and classifies them into arrhythmia types with severity levels.\n\n")
            
            f.write("## Dataset Analysis\n")
            f.write("### Training Dataset\n")
            f.write(f"- **Total Training Images**: {train_analysis['total_images']}\n")
            f.write(f"- **Number of Classes**: {len(train_analysis['classes'])}\n")
            f.write(f"- **Image Formats**: {list(train_analysis['image_formats'])}\n\n")
            
            f.write("#### Training Class Distribution\n")
            for class_code, count in train_analysis['classes'].items():
                class_info = self.preprocessor.class_mapping.get(class_code, {'name': 'Unknown'})
                f.write(f"- **{class_code} ({class_info['name']})**: {count} images\n")
            f.write("\n")
            
            f.write("### Test Dataset\n")
            f.write(f"- **Total Test Images**: {test_analysis['total_images']}\n")
            f.write(f"- **Number of Classes**: {len(test_analysis['classes'])}\n\n")
            
            f.write("#### Test Class Distribution\n")
            for class_code, count in test_analysis['classes'].items():
                class_info = self.preprocessor.class_mapping.get(class_code, {'name': 'Unknown'})
                f.write(f"- **{class_code} ({class_info['name']})**: {count} images\n")
            f.write("\n")
            
            f.write(f"### Combined Dataset Summary\n")
            f.write(f"- **Total Combined Images**: {train_analysis['total_images'] + test_analysis['total_images']}\n")
            f.write(f"- **Train/Test Split**: {train_analysis['total_images']}/{test_analysis['total_images']} ({train_analysis['total_images']/(train_analysis['total_images']+test_analysis['total_images'])*100:.1f}%/{test_analysis['total_images']/(train_analysis['total_images']+test_analysis['total_images'])*100:.1f}%)\n\n")
            
            f.write("## Classification Performance\n")
            f.write(f"- **Overall Accuracy**: {classification_results['accuracy']:.3f}\n\n")
            
            f.write("### Per-Class Performance\n")
            for class_name in class_names:
                if class_name in classification_results['classification_report']:
                    metrics = classification_results['classification_report'][class_name]
                    f.write(f"- **{class_name}**:\n")
                    f.write(f"  - Precision: {metrics['precision']:.3f}\n")
                    f.write(f"  - Recall: {metrics['recall']:.3f}\n")
                    f.write(f"  - F1-Score: {metrics['f1-score']:.3f}\n")
            f.write("\n")
            
            f.write("## Severity Prediction\n")
            f.write("The system predicts three severity levels for each detected arrhythmia:\n")
            f.write("- **Mild**: Low-risk cases requiring routine monitoring\n")
            f.write("- **Moderate**: Intermediate-risk cases requiring closer observation\n")
            f.write("- **Severe**: High-risk cases requiring immediate medical attention\n\n")
            
            # Severity distribution
            severity_dist = complete_results['severity_distribution']
            f.write("### Severity Distribution by Class\n")
            for class_name in severity_dist.index:
                f.write(f"- **{class_name}**:\n")
                total = severity_dist.loc[class_name].sum()
                for severity in ['Mild', 'Moderate', 'Severe']:
                    if severity in severity_dist.columns:
                        count = severity_dist.loc[class_name, severity]
                        percentage = (count / total * 100) if total > 0 else 0
                        f.write(f"  - {severity}: {count} ({percentage:.1f}%)\n")
            f.write("\n")
            
            f.write("## Clinical Significance\n")
            f.write("### Arrhythmia Types and Their Clinical Impact\n")
            for class_code, class_info in self.preprocessor.class_mapping.items():
                f.write(f"- **{class_code} - {class_info['name']}**: {class_info['description']}\n")
            f.write("\n")
            
            f.write("## System Capabilities\n")
            f.write("1. **Real-time ECG Analysis**: Process ECG images in real-time\n")
            f.write("2. **Multi-class Classification**: Identify 6 different types of cardiac conditions\n")
            f.write("3. **Severity Assessment**: Predict severity levels for prioritization\n")
            f.write("4. **Clinical Decision Support**: Provide actionable insights for healthcare providers\n")
            f.write("5. **Continuous Monitoring**: Enable ongoing patient monitoring\n\n")
            
            f.write("## File Outputs\n")
            f.write("- **Processed Data**: `processed/` directory\n")
            f.write("- **Trained Models**: `models/` directory\n")
            f.write("- **Analysis Reports**: `reports/` directory\n")
            f.write("- **Visualizations**: `visualizations/` directory\n\n")
            
            f.write("## Next Steps\n")
            f.write("1. Deploy models in clinical environment\n")
            f.write("2. Integrate with real-time ECG monitoring systems\n")
            f.write("3. Collect feedback from healthcare providers\n")
            f.write("4. Continuous model improvement and validation\n")
            f.write("5. Expand to additional arrhythmia types\n")
        
        print(f"📋 Comprehensive report saved to: {report_path}")
    
    def predict_single_ecg(self, image_path):
        """
        Predict classification and severity for a single ECG image
        
        Args:
            image_path (str): Path to ECG image
            
        Returns:
            dict: Prediction results
        """
        if self.classification_model is None:
            raise ValueError("Classification model not trained. Run complete pipeline first.")
        
        # Load and preprocess image
        image = self.preprocessor.load_and_preprocess_image(image_path)
        if image is None:
            return None
        
        # Classification prediction
        image_flat = image.reshape(1, -1)
        pred_class_idx = self.classification_model.predict(image_flat)[0]
        class_confidence = np.max(self.classification_model.predict_proba(image_flat))
        pred_class = self.preprocessor.label_encoder.inverse_transform([pred_class_idx])[0]
        
        # Severity prediction
        severity_label, severity_confidence, severity_name = self.severity_predictor.predict_severity(
            image, pred_class
        )
        
        # Get class description
        class_info = self.preprocessor.class_mapping.get(pred_class, {'name': 'Unknown', 'description': 'Unknown condition'})
        
        return {
            'image_path': image_path,
            'predicted_class': pred_class,
            'class_name': class_info['name'],
            'class_description': class_info['description'],
            'classification_confidence': class_confidence,
            'predicted_severity': severity_name,
            'severity_confidence': severity_confidence,
            'clinical_priority': self._get_clinical_priority(pred_class, severity_name)
        }
    
    def _get_clinical_priority(self, ecg_class, severity):
        """
        Determine clinical priority based on class and severity
        
        Args:
            ecg_class (str): ECG classification
            severity (str): Severity level
            
        Returns:
            str: Clinical priority level
        """
        high_risk_classes = ['M', 'V']  # MI and Ventricular arrhythmias
        
        if ecg_class in high_risk_classes and severity == 'Severe':
            return 'URGENT - Immediate medical attention required'
        elif ecg_class in high_risk_classes or severity == 'Severe':
            return 'HIGH - Close monitoring and medical evaluation needed'
        elif severity == 'Moderate':
            return 'MEDIUM - Regular monitoring recommended'
        else:
            return 'LOW - Routine follow-up sufficient'


def main():
    """
    Main function to run the complete RythmGuard pipeline
    """
    # Set data path
    data_path = r"d:\2nd-1st Sem\AI&ML\ECG_Image_data"
    
    # Initialize and run pipeline
    pipeline = RythmGuardPipeline(data_path, target_size=(224, 224))
    results = pipeline.run_complete_pipeline()
    
    # Example: Predict on a single image
    print("\n🔍 Example Single Image Prediction:")
    print("-" * 40)
    
    # Get a sample image path from test data
    test_dir = os.path.join(data_path, 'test')
    for class_folder in os.listdir(test_dir):
        class_path = os.path.join(test_dir, class_folder)
        if os.path.isdir(class_path):
            images = [f for f in os.listdir(class_path) if f.lower().endswith('.png')]
            if images:
                sample_image = os.path.join(class_path, images[0])
                prediction = pipeline.predict_single_ecg(sample_image)
                
                if prediction:
                    print(f"📁 Image: {os.path.basename(prediction['image_path'])}")
                    print(f"🏷️  Class: {prediction['predicted_class']} - {prediction['class_name']}")
                    print(f"📝 Description: {prediction['class_description']}")
                    print(f"🎯 Confidence: {prediction['classification_confidence']:.3f}")
                    print(f"⚕️  Severity: {prediction['predicted_severity']} (Confidence: {prediction['severity_confidence']:.3f})")
                    print(f"🚨 Priority: {prediction['clinical_priority']}")
                break
    
    print(f"\n✅ RythmGuard pipeline completed successfully!")
    print(f"📁 Check output directory: {pipeline.output_dir}")

if __name__ == "__main__":
    main()