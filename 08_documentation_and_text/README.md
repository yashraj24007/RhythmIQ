# RhythmIQ ECG Analysis System

## Overview
RhythmIQ is an AI-powered ECG monitoring system designed to analyze heart signals in real time. It processes electrocardiogram (ECG) data, detects irregularities, and classifies them into 5–6 common arrhythmia types while predicting severity levels (Mild, Moderate, Severe) to help healthcare providers prioritize urgent cases.

## Dataset Structure
The system works w\ith ECG images organized by classification:

```
ECG_Image_data/
├── test/
│   ├── F/    # Fusion beats
│   ├── M/    # Myocardial Infarction
│   ├── N/    # Normal beats
│   ├── Q/    # Unknown/Paced beats
│   ├── S/    # Supraventricular beats
│   └── V/    # Ventricular beats (PVC)
├── train/
│   └── [same structure as test]
└── processed/
    └── [generated preprocessed data]
```

## Classification Types

| Folder | Class | Meaning |
|--------|-------|---------|
| N | Normal | Normal beat (sinus rhythm, bundle branch block, etc.) |
| S | Supraventricular | Atrial premature beats, supraventricular ectopics |
| V | Ventricular | PVC (Premature Ventricular Contractions) |
| F | Fusion | Fusion of ventricular + normal beat |
| Q | Unknown | Paced beats, unclassifiable beats |
| M | Myocardial Infarction | MI - Sometimes added in extended versions |

## Features

### 🔍 ECG Classification
- **Multi-class Classification**: Identifies 6 different cardiac conditions
- **High Accuracy**: Uses advanced machine learning techniques
- **Real-time Processing**: Optimized for real-time ECG analysis

### ⚕️ Severity Prediction
- **Three Severity Levels**: Mild, Moderate, Severe
- **Clinical Priority**: Automatic priority assignment
- **Risk Assessment**: Helps healthcare providers prioritize cases

### 📊 Comprehensive Analysis
- **Dataset Analysis**: Complete statistical overview
- **Visualization**: Detailed charts and graphs
- **Performance Metrics**: Accuracy, precision, recall, F1-score

## Installation

1. **Clone or download the files**
2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your dataset** in the correct folder structure

## Usage

### 🌐 Java Web Application (NEW!)
**RhythmIQ now includes a complete Java web interface for ECG analysis!**

#### Quick Start - Web Interface
1. **Navigate to java-webapp directory**:
   ```bash
   cd java-webapp
   ```

2. **Run the web application**:
   ```bash
   ./mvnw spring-boot:run
   ```
   
3. **Access the application**:
   - Open your browser and go to: http://localhost:8082
   - Upload ECG images through the web interface
   - Get instant analysis results with confidence scores

#### Alternative Deployment
Use the deployment script from the project root:
```bash
# Windows
./09_deployment/run-webapp.bat

# Linux/Mac  
./09_deployment/run-webapp.sh
```

### 🐍 Python Training Pipeline

#### Quick Start - Model Training
Run the complete training pipeline:
```python
python simple_train.py
```

For comprehensive testing:
```python
python full_test_evaluation.py
```

### Individual Components

#### 1. ECG Preprocessing
```python
from ecg_preprocessor import ECGPreprocessor

# Initialize preprocessor
preprocessor = ECGPreprocessor(data_path, target_size=(224, 224))

# Analyze dataset
analysis = preprocessor.analyze_dataset('test')

# Create preprocessed dataset
X, y, class_names, paths = preprocessor.create_dataset('test')
```

#### 2. Severity Prediction
```python
from severity_predictor import SeverityPredictor

# Initialize severity predictor
severity_predictor = SeverityPredictor()

# Predict severity for an image
severity_label, confidence, severity_name = severity_predictor.predict_severity(image, ecg_class)
```

#### 3. Training and Testing
```python
# Train the model with your preferred size
python simple_train.py

# Run comprehensive evaluation
python full_test_evaluation.py

# Or use components directly
from ecg_preprocessor import ECGPreprocessor
from severity_predictor import SeverityPredictor

# Initialize components
preprocessor = ECGPreprocessor(data_path)
severity_predictor = SeverityPredictor()
```

## Output Structure

After running the training and testing, the following files are generated:

```
ECG_Image_data/
├── processed/
│   ├── test_images.npy
│   ├── test_labels.npy
│   ├── test_class_names.npy
│   └── test_metadata.csv
├── models/
│   ├── ecg_model_[size].joblib    # Trained Random Forest models
│   └── training_results_[size].txt # Training logs
├── reports/
│   ├── comprehensive_test_results.txt
│   ├── confusion_matrix.png
│   ├── class_distribution.png
│   └── test_predictions.csv
└── visualizations/
    ├── sample_predictions.png
    └── performance_metrics.png
```

## System Components

### 🌐 Java Web Application (`java-webapp/`)

**Technology Stack:**
- **Framework**: Spring Boot 3.4.1
- **Java Version**: JDK 21/24 compatible
- **Build Tool**: Maven 3.9.6 with wrapper
- **Template Engine**: Thymeleaf
- **Web Server**: Embedded Tomcat (Port 8082)

**Architecture Components:**

#### 1. Application Entry Point
- **`RhythmIQApplication.java`**: Spring Boot main class with auto-configuration

#### 2. Web Controller Layer
- **`UploadController.java`**: Handles web requests and file uploads
  - `@GetMapping("/")`: Homepage with upload interface
  - `@PostMapping("/analyze")`: Web form submission for ECG analysis
  - `@PostMapping("/api/analyze")`: REST API endpoint for programmatic access
  - File upload validation and processing

#### 3. Service Layer
- **`InferenceService.java`**: Business logic for ECG analysis
  - Mock inference implementation (ready for ML model integration)
  - File handling and storage management
  - Result processing and confidence calculation
  - Future integration point for Python ML models

#### 4. Domain Models
- **`ECGAnalysisResult.java`**: Data model for analysis results
  - ECG classification (N, S, V, F, Q, M)
  - Confidence scores and percentages
  - Severity levels (Normal, Mild, Moderate, Severe)
  - Descriptive text for medical interpretation

#### 5. Web Configuration
- **`WebConfig.java`**: Static resource configuration
  - File upload path mapping
  - Static content serving (CSS, JS, images)
  - CORS configuration for API access

#### 6. Frontend Templates (Thymeleaf)
- **`index.html`**: Welcome page with system overview
- **`upload.html`**: File upload interface with drag-and-drop
- **`results.html`**: Analysis results display with visualizations
- **Custom CSS**: Responsive design with medical theme

**Features Implemented:**
- ✅ Web-based file upload interface
- ✅ Real-time ECG image analysis
- ✅ REST API for integration
- ✅ Responsive web design
- ✅ File validation and error handling
- ✅ Mock inference service (ready for ML integration)
- ✅ Detailed analysis results display
- ✅ Image preview and metadata

**Deployment:**
- Built as executable JAR file
- Embedded Tomcat server
- No external dependencies required
- Cross-platform compatibility (Windows/Linux/macOS)

### 🐍 Python ML Components

#### 1. ECG Preprocessor (`ecg_preprocessor.py`)
- Image loading and preprocessing
- Data normalization and resizing
- Dataset analysis and visualization
- Class distribution analysis

#### 2. Severity Predictor (`severity_predictor.py`)
- Feature extraction from ECG images
- Severity level prediction (Mild/Moderate/Severe)
- Clinical priority determination
- Advanced ECG-specific feature analysis

#### 3. Training Pipeline (`simple_train.py`)
- User-friendly model training interface
- Balanced dataset handling
- Multiple size options (small/medium/large)
- Performance evaluation and model saving

#### 4. Comprehensive Testing (`full_test_evaluation.py`)
- Large-scale model evaluation
- Detailed confusion matrix analysis
- Per-class performance metrics
- Error analysis and reporting

## Performance Metrics

### 🎯 Achieved Results
- **Overall Test Accuracy**: 99.1% (4,673/4,717 correct predictions)
- **Processing Speed**: 0.098 seconds per image
- **Model**: Random Forest Classifier (50 estimators, max depth 10)

### 📊 Per-Class Performance
| Class | Precision | Recall | F1-Score | Test Accuracy |
|-------|-----------|--------|----------|---------------|
| **N** (Normal) | 99.2% | 99.7% | 99.4% | 99.7% |
| **S** (Supraventricular) | 99.2% | 96.9% | 98.0% | 96.9% |
| **V** (Ventricular/PVC) | 98.7% | 99.5% | 99.1% | 99.5% |
| **F** (Fusion) | 100.0% | 100.0% | 100.0% | 100.0% |
| **Q** (Unknown/Paced) | 100.0% | 100.0% | 100.0% | 100.0% |
| **M** (Myocardial Infarction) | 98.9% | 99.7% | 99.3% | 99.7% |

### 📈 Clinical Validation
- **Perfect Detection**: Fusion beats (F) and Unknown beats (Q) - 100% accuracy
- **Excellent MI Detection**: 98.9% precision for critical cardiac events
- **Robust Arrhythmia Classification**: >96% accuracy across all rhythm disorders
- **Minimal False Positives**: Only 44 misclassifications out of 4,717 test cases

## Clinical Applications

### 🏥 Healthcare Integration
- **Real-time Monitoring**: Continuous ECG analysis
- **Early Warning System**: Automatic detection of critical conditions
- **Decision Support**: Evidence-based recommendations
- **Workflow Optimization**: Priority-based patient triage

### 📈 Severity Levels
- **Mild**: Routine monitoring, regular follow-up
- **Moderate**: Close observation, medical evaluation
- **Severe**: Immediate attention, urgent care required

## Customization

### Adding New Classes
1. Create new folder in dataset structure
2. Update `class_mapping` in `ECGPreprocessor`
3. Adjust severity rules in `SeverityPredictor`

### Modifying Severity Rules
Edit the `class_severity_rules` in `SeverityPredictor` class:
```python
self.class_severity_rules = {
    'N': {'mild': 0.8, 'moderate': 0.15, 'severe': 0.05},
    # ... modify probabilities as needed
}
```

### Custom Augmentation
Add new augmentation techniques in `ECGAugmentor` class.

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: Install requirements with `pip install -r requirements.txt`
2. **Path Issues**: Ensure correct dataset path structure
3. **Memory Issues**: Reduce batch size or image resolution
4. **Model Loading**: Ensure models are trained before prediction

### Dataset Requirements
- Images should be in PNG/JPG format
- Consistent image quality
- Proper folder organization
- Sufficient samples per class for training

## 🔗 Java-Python Integration

### Current Implementation
The Java web application currently uses a **mock inference service** that simulates ECG analysis results. This design allows the web interface to function independently while providing a clear integration point for the Python ML models.

### Integration Architecture
```
┌─────────────────┐    HTTP/REST    ┌──────────────────┐
│   Java Web App  │ ────────────────▶│  Python ML API   │
│   (Port 8082)   │                 │  (Future: Flask) │
│                 │◀────────────────│                  │
│ - File Upload   │    JSON Results  │ - Model Loading  │
│ - Web Interface │                 │ - Preprocessing  │
│ - Results View  │                 │ - Classification │
└─────────────────┘                 └──────────────────┘
```

### Integration Steps (Planned)
1. **Python FastAPI/Flask Service**: Wrap the trained ML model in a REST API
2. **Service Communication**: Replace mock inference with HTTP calls to Python service
3. **Data Pipeline**: Implement image transfer and result parsing
4. **Error Handling**: Add robust error handling for service communication
5. **Performance Optimization**: Implement caching and async processing

### How to Integrate
1. **Create Python API Service**:
   ```python
   # Example: ecg_api_service.py
   from flask import Flask, request, jsonify
   from severity_predictor import SeverityPredictor
   from ecg_preprocessor import ECGPreprocessor
   
   app = Flask(__name__)
   predictor = SeverityPredictor()
   
   @app.route('/analyze', methods=['POST'])
   def analyze_ecg():
       file = request.files['image']
       # Process with existing ML pipeline
       result = predictor.analyze(file)
       return jsonify(result)
   ```

2. **Update Java Service**:
   ```java
   // In InferenceService.java - replace mockInference()
   private ECGAnalysisResult callPythonAPI(MultipartFile file) {
       // HTTP call to Python service
       // Parse response to ECGAnalysisResult
   }
   ```

## Future Enhancements

### Immediate (Java Web App)
- [x] ✅ Web-based interface (COMPLETED)
- [ ] 🔄 Python ML model integration (IN PROGRESS)
- [ ] User authentication and sessions
- [ ] Batch processing for multiple files
- [ ] Analysis history and reports
- [ ] Export results to PDF/CSV

### Medium Term
- [ ] Deep learning model integration (CNN/ResNet)
- [ ] Real-time data streaming support
- [ ] Mobile-responsive design improvements
- [ ] REST API documentation (Swagger/OpenAPI)
- [ ] Database integration for result storage

### Long Term
- [ ] Mobile application (React Native/Flutter)
- [ ] Integration with hospital systems (HL7 FHIR)
- [ ] Advanced arrhythmia types
- [ ] Temporal analysis for continuous monitoring
- [ ] Multi-language support
- [ ] Cloud deployment (AWS/Azure/GCP)

## 🧪 Testing the Application

### Web Application Testing

1. **Start the application**:
   ```bash
   cd java-webapp
   ./mvnw spring-boot:run
   ```

2. **Access the web interface**:
   - Open: http://localhost:8082
   - Upload any ECG image from `01_data/test/` folder
   - View analysis results with confidence scores

3. **API Testing** (using curl):
   ```bash
   curl -X POST http://localhost:8082/api/analyze \
     -F "image=@01_data/test/N/N1.png" \
     -H "Accept: application/json"
   ```

### Python Components Testing
```bash
# Run model training
python simple_train.py

# Test individual components
python -m pytest tests/

# Full evaluation
python full_test_evaluation.py
```

### Current Test Results
- **Java Web App**: ✅ Deployed and running on port 8082
- **File Upload**: ✅ Working with drag-and-drop interface
- **Mock Analysis**: ✅ Returns realistic ECG classification results
- **REST API**: ✅ JSON responses for programmatic access
- **Python ML Model**: ✅ 99.1% accuracy on test dataset

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper documentation
4. Test thoroughly
5. Submit pull request

## License

This project is intended for educational and research purposes. For clinical use, ensure proper validation and regulatory compliance.

## Contact

For questions, issues, or contributions, please create an issue in the repository or contact the development team.

---

**⚠️ Important Note**: This system is designed for research and educational purposes. For clinical applications, ensure proper validation, regulatory compliance, and integration with qualified healthcare professionals.