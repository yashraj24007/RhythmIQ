# RhythmIQ - Organized Folder Structure

This document outlines the organized folder structure for the RhythmIQ ECG Analysis project.

## 📁 Project Structure

```text
RhythmIQ/
├── 01_data/                    # Training and testing ECG data
│   ├── train/                  # Training images (6 classes: N,S,V,F,Q,M)
│   └── test/                   # Testing images for validation
│
├── 02_preprocessing/           # Data preprocessing modules
│   ├── ecg_preprocessor.py     # ECG image preprocessing utilities
│   └── ecg_augmentor.py        # Data augmentation techniques
│
├── 03_model_training/          # Model training and pipeline
│   ├── rythmguard_pipeline.py  # Main training pipeline
│   ├── severity_predictor.py   # Severity classification module
│   ├── simple_train.py         # Simple training script
│   ├── quick_train_test.py     # Quick training and testing
│   └── training_readiness_check.py # Pre-training validation
│
├── 04_model_evaluation/        # Model testing and evaluation
│   ├── test_model.py           # Basic model testing
│   ├── full_test_evaluation.py # Comprehensive evaluation
│   ├── test_trained_model.py   # Trained model validation
│   ├── test_with_images.py     # Image-based testing
│   ├── verify_train_test.py    # Training verification
│   └── model_test_report.txt   # Latest test results
│
├── 05_trained_models/          # Trained model files
│   └── rythmguard_model.joblib # Main production model (99.1% accuracy)
│
├── 06_web_application/         # Web application components
│   ├── java-webapp/           # Spring Boot web application
│   └── test_single_image.py   # Python integration script
│
├── 07_results_visualizations/ # Generated plots and visualizations
│   ├── confusion_matrix.png          # Model confusion matrix
│   ├── full_test_confusion_matrix.png # Full test results
│   ├── test_confusion_matrix.png     # Test confusion matrix
│   ├── sample_ecg_preview.png        # Sample ECG visualization
│   └── severity_predictions_sample.png # Severity prediction examples
│
├── 08_documentation/          # Project documentation
│   ├── quick_demo.py          # Quick demonstration script
│   └── JAVA_WEB_APP_GUIDE.md  # Java web application guide
│
├── 09_deployment/             # Deployment scripts and configurations
│   ├── run-webapp.bat         # Windows webapp launcher
│   ├── start-webapp.bat       # Windows startup script
│   └── run-webapp.sh          # Unix webapp launcher
│
├── tests/                     # Unit tests
│   ├── test_ecg_preprocessor.py    # Preprocessor tests
│   ├── test_ecg_augmentor.py       # Augmentor tests
│   ├── test_severity_predictor.py  # Severity predictor tests
│   ├── test_model_validation.py    # Model validation tests
│   └── test_hello_world.py         # Basic test example
│
├── README.md                  # Main project documentation
├── requirements.txt           # Python dependencies
├── pytest.ini               # Pytest configuration
└── FOLDER_STRUCTURE.md       # This file
```

## 🎯 Model Performance

- **Overall Test Accuracy**: **99.1%** (4,673/4,717 correct predictions)
- **ECG Classifications**: 6 classes (N, S, V, F, Q, M)
- **Severity Levels**: 3 levels (Low, Medium, High risk)

## 🚀 Quick Start

1. **Model Training**: Run scripts in `03_model_training/`
2. **Model Testing**: Use scripts in `04_model_evaluation/`
3. **Web Application**: Launch from `06_web_application/java-webapp/`
4. **Results Review**: Check visualizations in `07_results_visualizations/`

## 🔗 Integration

- **Python Backend**: Located in organized folders by function
- **Java Web App**: Spring Boot application in `06_web_application/`
- **Model Files**: Centralized in `05_trained_models/`
- **Documentation**: Comprehensive guides in `08_documentation/`

## 📊 Recent Changes

- ✅ Organized all files into sequential, logical folders
- ✅ Updated model accuracy to 99.1% throughout codebase
- ✅ Removed redundant and cache files
- ✅ Updated path references in integration scripts
- ✅ Centralized model storage and documentation

This structure provides a clear, maintainable, and professional organization for the RhythmIQ project.