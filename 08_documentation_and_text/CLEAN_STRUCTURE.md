# 🫀 RhythmIQ - Organized Project Structure

## 📂 Clean Directory Organization

```
RhythmIQ/
├── 📊 01_data/                    # ECG Dataset (Reduced Size)
│   ├── train/                     # Training images (50 per class)
│   │   ├── F/ M/ N/ Q/ S/ V/      # 6 ECG classes
│   └── test/                      # Test images (5 per class)
│       └── F/ M/ N/ Q/ S/ V/      # 6 ECG classes
│
├── 🔧 02_preprocessing/           # Data Processing
│   ├── ecg_augmentor.py          # Image augmentation
│   └── ecg_preprocessor.py       # Image preprocessing
│
├── 🎯 03_model_training/         # ML Model Training
│   ├── rythmguard_pipeline.py    # Complete training pipeline
│   ├── severity_predictor.py     # Severity assessment
│   ├── simple_train.py           # Simple training script
│   ├── quick_train_test.py       # Quick training test
│   └── training_readiness_check.py
│
├── 🧪 04_model_evaluation/       # Model Testing
│   ├── full_test_evaluation.py   # Comprehensive testing
│   ├── test_model.py             # Model validation
│   └── test_trained_model.py     # Trained model tests
│
├── 🤖 05_trained_models/         # Trained ML Models
│   └── rythmguard_model.joblib   # Main ECG classifier
│
├── 📊 07_results_visualizations/ # (Empty - cleaned)
│
├── 🚀 09_deployment/            # Deployment Scripts
│   ├── run-webapp.bat           # Windows webapp runner
│   ├── run-webapp.sh            # Unix webapp runner
│   ├── start-webapp.bat         # Webapp starter
│   ├── start-full-system.bat    # Full system (Windows)
│   ├── start-full-system.sh     # Full system (Unix)
│   ├── start-java-webapp.bat    # Java webapp only
│   ├── start_java_webapp.bat    # Java webapp variant
│   ├── start_rhythmiq.bat       # RhythmIQ starter
│   ├── run-app.bat              # App runner
│   └── verify_deployment_setup.sh
│
├── 🐍 10_python_api/           # Python ML API Service
│   ├── rhythmiq_api.py          # Flask API server
│   └── requirements.txt         # API dependencies
│
├── 📚 11_documentation/         # Project Documentation
│   ├── PROJECT_STRUCTURE.md     # This file (moved here)
│   └── QUICK_START_GUIDE.md     # Quick start guide
│
├── ⚙️  12_config/              # Configuration Files
│   ├── requirements.txt         # Main Python dependencies
│   └── pytest.ini             # Test configuration
│
├── 🌐 java-webapp/             # Java Web Application
│   ├── src/main/java/          # Java source code
│   ├── src/main/resources/     # Web templates & static files
│   ├── target/                 # Compiled JAR file
│   ├── pom.xml                # Maven configuration
│   ├── README.md              # Java webapp docs
│   └── DEPLOYMENT_SUMMARY.md   # Deployment guide
│
├── 🧪 tests/                   # Unit Tests
│   ├── test_ecg_augmentor.py   # Augmentation tests
│   ├── test_ecg_preprocessor.py # Preprocessing tests
│   ├── test_hello_world.py     # Basic tests
│   ├── test_model_validation.py # Model validation tests
│   ├── test_severity_predictor.py # Severity prediction tests
│   └── test_single_image.py    # Single image test
│
└── 📄 Root Files
    ├── README.md               # Main project documentation
    └── .gitignore             # Git ignore rules
```

## 🎯 Key Benefits

### ✅ Organized Structure
- **Logical grouping**: Files organized by function
- **Clear separation**: API, webapp, data, docs separate
- **Easy navigation**: Numbered folders for workflow order
- **Clean root**: Only essential files in main directory

### ✅ Reduced Size
- **Dataset**: Reduced from 90k+ to 330 images (50 train + 5 test per class)
- **No duplicates**: Removed redundant files and matrices
- **Essential only**: Kept only production-ready components
- **Fast operations**: Quicker builds, tests, and deployments

### ✅ Production Ready
- **Deployable**: Ready for containerization and cloud deployment
- **Maintainable**: Clean codebase without clutter
- **Scalable**: Easy to add new features and components
- **Professional**: Industry-standard organization

## 🚀 How to Use

### 1. Start Python API
```bash
cd 10_python_api
pip install -r requirements.txt
python rhythmiq_api.py
```

### 2. Start Java Webapp
```bash
cd java-webapp
java -jar target/rhythmiq-webapp-1.0.0.jar
```

### 3. Or Use Deployment Scripts
```bash
cd 09_deployment
# Windows
start-full-system.bat

# Unix/Linux
./start-full-system.sh
```

### 4. Access Application
- **Web Interface**: http://localhost:8082
- **Python API**: http://localhost:8083
- **Upload ECG**: Upload ECG images for real-time analysis

## 📈 System Flow

```
Upload ECG Image → Java Webapp (8082) → Python API (8083) → ML Model → Results
```

The system is now **clean**, **organized**, and **ready for production deployment**! 🎉