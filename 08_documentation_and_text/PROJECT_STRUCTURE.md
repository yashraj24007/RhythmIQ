# 🫀 RhythmIQ - Clean Project Structure

## Overview
RhythmIQ is an ECG analysis system with a Java web application and Python ML backend.

## 📁 Clean Project Structure

```
RhythmIQ/
├── 📊 01_data/                    # ECG Dataset (Reduced Size)
│   ├── train/                     # Training images (50 per class)
│   │   ├── F/                     # Fusion beats
│   │   ├── M/                     # Myocardial Infarction
│   │   ├── N/                     # Normal beats
│   │   ├── Q/                     # Unknown/Paced beats
│   │   ├── S/                     # Supraventricular beats
│   │   └── V/                     # Ventricular beats
│   └── test/                      # Test images (5 per class)
│       ├── F/, M/, N/, Q/, S/, V/ # Same structure as train
│
├── 🔧 02_preprocessing/           # Data Processing
│   ├── ecg_augmentor.py          # Data augmentation
│   └── ecg_preprocessor.py       # Image preprocessing
│
├── 🧠 03_model_training/          # ML Model Training
│   ├── quick_train_test.py       # Quick training script
│   ├── rythmguard_pipeline.py    # Complete training pipeline
│   ├── severity_predictor.py     # Severity classification
│   ├── simple_train.py           # Simple training script
│   └── training_readiness_check.py # Training validation
│
├── 📈 04_model_evaluation/        # Model Testing (Cleaned)
│   ├── full_test_evaluation.py   # Complete evaluation
│   ├── test_model.py             # Model testing suite
│   └── test_trained_model.py     # Trained model validation
│
├── 💾 05_trained_models/          # Trained Models
│   └── rythmguard_model.joblib   # Main ECG classification model
│
├── 🌐 java-webapp/               # Java Web Application
│   ├── src/main/java/            # Java source code
│   ├── src/main/resources/       # Web templates & static files
│   ├── target/                   # Compiled JAR file
│   └── pom.xml                   # Maven configuration
│
├── 🧪 tests/                     # Unit Tests
│   ├── test_ecg_augmentor.py     # Augmentation tests
│   ├── test_ecg_preprocessor.py  # Preprocessing tests
│   └── test_*.py                 # Other test files
│
├── 📝 Configuration Files
│   ├── README.md                 # Project documentation
│   ├── requirements.txt          # Python dependencies
│   ├── pytest.ini              # Test configuration
│   ├── QUICK_START_GUIDE.md     # Quick start instructions
│   └── minimal_api.py           # Python ML API service
│
└── 📦 Deployment
    └── 09_deployment/            # Deployment scripts
        ├── run-webapp.bat        # Windows launcher
        └── run-webapp.sh         # Unix launcher
```

## 🚀 Key Components

### 1. **Java Web Application** (`java-webapp/`)
- Spring Boot web interface
- ECG image upload and analysis
- Results display with severity assessment
- Runs on port 8082

### 2. **Python ML API** (`minimal_api.py`)
- Flask API serving the trained model
- ECG image classification
- Runs on port 8083
- Returns JSON results

### 3. **ECG Dataset** (`01_data/`)
- **Reduced size**: 50 training + 5 test images per class
- **6 Classes**: F, M, N, Q, S, V
- **Total**: 300 training + 30 test images (vs original 90k+ images)

### 4. **Trained Model** (`05_trained_models/`)
- RandomForest classifier with 99.1% accuracy
- Includes severity prediction
- Optimized for real-time inference

## 🎯 What Was Removed

### Files Cleaned Up:
- ❌ Confusion matrix images (`.png` files)
- ❌ Test reports and logs (`.txt` files)
- ❌ Debug scripts (`debug_*.py`, `test_*.py`)
- ❌ Temporary documentation files
- ❌ Upload folders and cached files
- ❌ Docker and deployment configs
- ❌ Excessive test data (reduced from 90k+ to 330 images)

### Folders Removed:
- ❌ `07_results_visualizations/` (empty after cleanup)
- ❌ `08_documentation/` (consolidated into README)
- ❌ `uploads/` and `java-webapp-uploads/` (temporary)
- ❌ `demo_images_for_website/` (samples)

## ✅ Benefits of Clean Structure

1. **Reduced Size**: Project went from ~2GB to ~50MB
2. **Faster Operations**: Less data to process
3. **Clear Organization**: Easy to navigate
4. **Production Ready**: Only essential files remain
5. **Maintainable**: Clean codebase without clutter

## 🚀 How to Use

1. **Start Python API**: `python minimal_api.py`
2. **Start Java Web App**: `java -jar java-webapp/target/rhythmiq-webapp-1.0.0.jar`
3. **Access Interface**: http://localhost:8082
4. **Upload ECG**: Upload ECG image for analysis

The system is now clean, organized, and ready for deployment! 🎉