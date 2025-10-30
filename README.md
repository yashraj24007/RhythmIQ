# 🫀 RhythmIQ - AI-Powered ECG Analysis Platform

[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/yashraj24007/RhythmIQ)
[![Java](https://img.shields.io/badge/Java-21-orange)](https://www.oracle.com/java/)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4.1-green)](https://spring.io/projects/spring-boot)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

> **Professional ECG analysis powered by machine learning** - Instantly classify cardiac rhythms with 83.3% accuracy using advanced AI algorithms.

## 🌟 Overview

RhythmIQ is a sophisticated medical-grade ECG analysis platform that combines modern web technologies with powerful machine learning to provide instant cardiac rhythm classification. Our system analyzes electrocardiogram images and identifies 6 different rhythm types with high accuracy.

### ✨ Key Features

- 🤖 **AI-Powered Analysis** - RandomForest classifier with 83.3% accuracy
- 📊 **6 Rhythm Types** - F (Fusion), M (Myocardial), N (Normal), Q (Q-wave), S (Supraventricular), V (Ventricular)
- 🎨 **Modern UI** - Professional interface with Stormy/Cloud/Sunset/Evening color palette
- 🌓 **Dark Mode** - Comfortable viewing in any lighting condition
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🔒 **Medical Disclaimer** - Clear warnings for professional use only
- 📚 **Educational Content** - Comprehensive ECG guide for learning

## 🚀 Quick Start

### Prerequisites

- **Java 21** or higher
- **Python 3.13** or higher
- **Maven 3.9+** (included via wrapper)

### Installation

```powershell
# Clone the repository
git clone https://github.com/yashraj24007/RhythmIQ.git
cd RhythmIQ

# Start the application (automatically starts both services)
.\start-services.ps1
```

The application will be available at:
- **Web Application**: http://localhost:8082
- **Python ML API**: http://localhost:8083/health

### Stopping Services

```powershell
.\stop-services.ps1
```

## 📁 Project Structure

```
RhythmIQ/
├── 📊 01_data/                      # ECG image datasets (train/test)
├── 🔬 02_preprocessing/             # ECG preprocessing modules
├── 🧠 03_model_training/            # ML model training scripts
├── 📈 04_model_evaluation/          # Model testing & evaluation
├── 💾 05_trained_models/            # Trained RandomForest model (83.3% accuracy)
├── 📸 06_results_visualizations/    # Confusion matrices & sample predictions
├── ☕ 07_java_webapp/               # Spring Boot web application (Port 8082)
│   ├── src/main/
│   │   ├── java/com/rhythmiq/      # Controllers, Services, Models
│   │   └── resources/
│   │       ├── templates/           # Thymeleaf HTML pages
│   │       └── static/             # CSS, JS, images
│   └── target/                     # Built JAR file
├── 📚 08_documentation_and_text/   # All project documentation
├── 🧪 09_tests/                    # Python & PowerShell test scripts
├── 🚀 10_deployment/               # Deployment configs & scripts
├── 🐍 11_python_api/               # Flask ML API (Port 8083)
├── start-services.ps1              # Quick start script
├── stop-services.ps1               # Stop all services
├── render.yaml                     # Cloud deployment config
└── requirements-api.txt            # Python dependencies
```

## 🎨 Technology Stack

### Frontend
- **Framework**: Spring Boot 3.4.1 + Thymeleaf
- **Styling**: Custom CSS with Stormy/Cloud/Sunset/Evening palette
- **Features**: Responsive design, dark mode, drag-and-drop upload

### Backend Services
- **Web Server**: Spring Boot (Java 21) - Port 8082
- **ML API**: Flask (Python 3.13) - Port 8083
- **ML Model**: RandomForest Classifier - 83.3% accuracy

### Machine Learning
- **Algorithm**: Random Forest
- **Features**: Image preprocessing, data augmentation
- **Classes**: 6 ECG rhythm types (F, M, N, Q, S, V)
- **Accuracy**: 83.3% on test dataset

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Overall Accuracy | 83.3% |
| Training Images | 1,000+ |
| Test Images | 250+ |
| Model Type | RandomForest |
| Classes | 6 (F, M, N, Q, S, V) |

## 🌐 Pages

- **Home** - Professional landing page with hero section
- **Dashboard** - Quick stats and action cards
- **Analyze ECG** - Upload and analyze ECG images
- **ECG Guide** - Educational content about 6 rhythm types
- **About** - Company information and mission

## 🔧 Development

### Build from Source

```powershell
# Build Java application
cd 07_java_webapp
.\mvnw.cmd clean package -DskipTests
cd ..

# Start services
.\start-services.ps1
```

### Running Tests

```powershell
# Python tests
pytest 09_tests/ -v

# Test all ECG classes
.\09_tests\test_all_classes.ps1
```

## 🚀 Deployment

### Deploy to Render.com (Recommended)

1. Push code to GitHub
2. Create Render account at https://render.com
3. Create new "Blueprint" and connect GitHub repository
4. Render will automatically detect `render.yaml` and deploy both services

### Deploy to Railway.app

```powershell
npm i -g @railway/cli
railway login
railway init
railway up
```

### Docker Deployment

```powershell
docker-compose up -d
```

See [`08_documentation_and_text/DEPLOYMENT_GUIDE.md`](08_documentation_and_text/DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## 📖 Documentation

All documentation is available in the `08_documentation_and_text/` folder:

- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **PROJECT_ORGANIZATION.md** - Detailed project structure
- **PROFESSIONAL_REDESIGN.md** - UI/UX design documentation
- **ECG_GUIDE_FEATURE.md** - ECG educational content details

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

**Yashraj Patil**
- GitHub: [@yashraj24007](https://github.com/yashraj24007)
- Repository: [RhythmIQ](https://github.com/yashraj24007/RhythmIQ)

## 🙏 Acknowledgments

- ECG dataset providers
- Spring Boot and Flask communities
- Machine learning libraries (scikit-learn, NumPy, Pillow)
- Medical professionals who validated the educational content

---

<div align="center">

**Made with ❤️ by Yashraj Patil**

⭐ Star this repository if you find it helpful!

</div>
