# 🫀 RhythmIQ - AI-Powered ECG Analysis Platform

[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/yashraj24007/RhythmIQ)
[![Java](https://img.shields.io/badge/Java-21-orange)](https://www.oracle.com/java/)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4.1-green)](https://spring.io/projects/spring-boot)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

> **Professional ECG analysis powered by machine learning** - Instantly classify cardiac arrhythmias using advanced AI algorithms with microservices architecture.

## 🌟 Overview

RhythmIQ is a sophisticated ECG analysis platform that combines modern web technologies with powerful machine learning to provide instant cardiac rhythm classification. Built with a microservices architecture, the system analyzes electrocardiogram images and identifies 6 different arrhythmia types with high accuracy.

### ✨ Key Features

- 🤖 **AI-Powered Analysis** - RandomForest/CNN classifier for accurate arrhythmia detection
- 🏗️ **Microservices Architecture** - Separate Java webapp and Python ML API services
- 💓 **6 Arrhythmia Types** - Normal (N), Atrial Fibrillation (F), Atrial Flutter (M), AV Block (Q), Supraventricular (S), Ventricular (V)
- 🎨 **Modern UI** - Clean, professional interface with responsive design
- ⚡ **Real-time Processing** - Fast image analysis with confidence scores
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- � **One-Click Startup** - Simple batch file to launch entire system
- 📚 **Educational Content** - Comprehensive ECG guide for learning

## 🚀 Quick Start

### Prerequisites

- ☕ **Java 21** or higher
- 🐍 **Python 3.13** or higher
- 📦 **Maven** (included via wrapper)

### Installation & Startup

```bash
# 1. Clone the repository
git clone https://github.com/yashraj24007/RhythmIQ.git
cd RhythmIQ

# 2. Install Python dependencies
pip install -r 09_python_api/requirements.txt

# 3. Start everything with ONE command!
START_RHYTHMIQ.bat
```

**That's it!** 🎉 The script will automatically:
- ✅ Start Python ML API on port 8083
- ✅ Start Java Web Application on port 8082
- ✅ Open your browser to http://localhost:8082
- ✅ Both services run in parallel (no visible terminals)

### Accessing the Application

Once started, access:
- 🌐 **Web Interface**: http://localhost:8082
- 🔬 **ML API Health**: http://localhost:8083/health

### Stopping Services

```powershell
# Option 1: Use stop script
cd 08_deployment
.\stop-services.ps1

# Option 2: Kill processes manually
taskkill /F /IM java.exe
taskkill /F /IM python.exe
```

## 📁 Project Structure

```
RhythmIQ/
├── 📊 01_data/                      # ECG image datasets
│   ├── train/                       # Training data (F, M, N, Q, S, V)
│   ├── test/                        # Test data (F, M, N, Q, S, V)
│   └── rythmguard_model.joblib      # Trained ML model
├── 🔬 02_preprocessing/             # ECG preprocessing modules
│   ├── ecg_preprocessor.py          # Image preprocessing
│   └── ecg_augmentor.py             # Data augmentation
├── 🧠 03_model_training/            # ML model training scripts
│   └── rythmguard_pipeline.py       # Training pipeline
├── 🧠 03_model_training/            # ML model training scripts
│   ├── simple_train.py              # Main training script
│   ├── severity_predictor.py        # Severity analysis
│   └── training_readiness_check.py  # Pre-training validation
├── 📈 04_model_evaluation/          # Model testing & evaluation
│   ├── test_model.py                # Model testing
│   └── full_test_evaluation.py      # Comprehensive evaluation
├── 💾 05_trained_models/            # Trained RandomForest model (100% accuracy)
│   └── rythmguard_model.joblib      # Production model (203 KB)
├── ☕ 06_java_webapp/               # Spring Boot web application (Port 8082)
│   ├── src/main/
│   │   ├── java/com/rhythmiq/       # Controllers, Services, Models
│   │   │   ├── config/              # SupabaseConfig (loads .env)
│   │   │   ├── service/             # SupabaseAuthService
│   │   │   └── controller/          # AuthController, HomeController
│   │   └── resources/
│   │       ├── templates/           # Thymeleaf HTML pages
│   │       │   ├── dashboard.html   # Main dashboard
│   │       │   ├── upload.html      # ECG upload interface
│   │       │   ├── results.html     # Analysis results
│   │       │   ├── index.html       # Landing page
│   │       │   └── ...              # Other pages
│   │       ├── static/css/          # Stylesheets
│   │       └── application.properties # Spring Boot config
│   ├── pom.xml                      # Maven dependencies
│   └── target/                      # Built JAR (rhythmiq-webapp-1.0.0.jar)
├── 🧪 07_tests/                    # Test scripts
│   ├── test_ecg_preprocessor.py     # Unit tests
│   └── test_integration.ps1         # Integration tests
├── 🚀 08_deployment/               # Deployment scripts (SIMPLIFIED!)
│   ├── start-services.ps1           # Main startup script
│   ├── stop-services.ps1            # Stop all services
│   └── DEPLOYMENT_GUIDE.md          # Deployment documentation
├── 🐍 09_python_api/               # Flask ML API (Port 8083)
│   ├── rhythmiq_api.py              # Main API server
│   └── requirements.txt             # Python dependencies
├── START_RHYTHMIQ.bat               # ⭐ ONE-CLICK STARTUP! ⭐
└── README.md                        # This file
```

## 🎨 Technology Stack

### Frontend
- **Framework**: Spring Boot 3.4.1 + Thymeleaf
- **Styling**: Custom CSS with modern responsive design
- **Features**: File upload, real-time analysis, results display
- **UI/UX**: Clean interface with intuitive navigation

### Backend Architecture (Microservices)
- **Web Application**: Spring Boot (Java 21) - Port 8082
  - Handles HTTP requests, file uploads, UI rendering
  - Communicates with ML API via REST
- **ML API Service**: Flask (Python 3.13) - Port 8083
  - Processes ECG images
  - Runs ML model inference
  - Returns predictions with confidence scores
- **Communication**: RESTful APIs with JSON

### Machine Learning
- **Algorithm**: Random Forest / CNN
- **Framework**: scikit-learn, OpenCV, NumPy
- **Features**: Image preprocessing, feature extraction
- **Classes**: 6 arrhythmia types (Normal, AFib, Flutter, AV Block, Supraventricular, Ventricular)
- **Processing**: Real-time inference with confidence scoring
- **Model Format**: Joblib serialized model

## 🌐 Application Features

### Core Pages
- **Home** (`/`) - Landing page with system overview
- **Dashboard** (`/dashboard`) - Main control panel
- **Upload** (`/upload`) - ECG image upload interface
- **Results** (`/results`) - Analysis results with confidence scores
- **ECG Guide** (`/ecg-guide`) - Educational content about arrhythmia types
- **About** (`/about`) - System information

### Key Features
- ✅ **Drag & Drop Upload** - Easy ECG image submission
- ✅ **Real-time Analysis** - Instant ML predictions (2-4 seconds)
- ✅ **Confidence Scores** - Transparency in predictions
- ✅ **6 Arrhythmia Types** - Comprehensive classification
- ✅ **Responsive Design** - Works on all devices
- ✅ **No Authentication Required** - Direct access enabled

## 🔧 Development

### Build from Source

```powershell
# Build Java application
cd 06_java_webapp
.\mvnw.cmd clean package -DskipTests
cd ..

# Ensure .env file is configured with your Supabase credentials
# Then start services
.\start-services.ps1
```

### Running Tests

```powershell
# Python unit tests
pytest 07_tests/ -v

# Test integration
.\07_tests\test_integration.ps1
```

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────┐
│              User Browser                        │
│           (localhost:8082)                       │
└───────────────────┬──────────────────────────────┘
                    │ HTTP Requests
                    ▼
         ┌─────────────────────┐
         │  Java Web App       │
         │  Spring Boot        │
         │  Port 8082          │
         │ ─────────────────── │
         │ • File Upload       │
         │ • UI Rendering      │
         │ • Request Routing   │
         └──────────┬──────────┘
                    │ REST API (POST /analyze)
                    ▼
         ┌─────────────────────┐
         │  Python ML API      │
         │  Flask              │
         │  Port 8083          │
         │ ─────────────────── │
         │ • Image Processing  │
         │ • ML Inference      │
         │ • Feature Extract   │
         └──────────┬──────────┘
                    │ Model Load
                    ▼
         ┌─────────────────────┐
         │  ML Model           │
         │  (.joblib)          │
         │  6 Classes          │
         └─────────────────────┘
```

## 🎯 Use Cases

- 🏥 **Medical Professionals** - Quick ECG rhythm analysis
- 📚 **Students** - Learning about different arrhythmia types
- 🔬 **Researchers** - Testing ECG classification algorithms
- 🏢 **Healthcare Facilities** - Automated preliminary screening

## 📖 Documentation

Documentation is included in this README file. For additional support:

- Check the inline code comments in each module
- Review the test scripts in `07_tests/` for usage examples
- See deployment scripts in `08_deployment/` for setup instructions
- Environment configuration: See `.env.example` for template

### Key Configuration Files

- **pom.xml**: Maven dependencies (Supabase, JWT, Spring Security)
- **application.properties**: Spring Boot configuration with environment variables
- **render.yaml**: Cloud deployment configuration
- **.env**: Local environment variables (create from `.env.example`)

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for educational and research purposes only. It is NOT intended for clinical diagnosis or medical decision-making. Always consult qualified healthcare professionals for medical advice and ECG interpretation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Yash Raj**
- GitHub: [@yashraj24007](https://github.com/yashraj24007)
- Repository: [RhythmIQ](https://github.com/yashraj24007/RhythmIQ)

## 🙏 Acknowledgments

- ECG dataset providers
- Spring Boot and Flask communities
- Machine learning libraries (scikit-learn, NumPy, Pillow)
- Medical professionals who validated the educational content

---

<div align="center">

**Made with ❤️ by Yash Raj**

</div>
