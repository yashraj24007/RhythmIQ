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

- 🤖 **AI-Powered Analysis** - RandomForest classifier with 100% accuracy
- 🔐 **Supabase Authentication** - Secure user registration and login with JWT tokens
-  **6 Rhythm Types** - F (Fusion), M (Myocardial), N (Normal), Q (Q-wave), S (Supraventricular), V (Ventricular)
- 🎨 **Modern UI** - Professional interface with Stormy/Cloud/Sunset/Evening color palette
- 🌓 **Dark Mode** - Comfortable viewing in any lighting condition
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🔒 **Secure Environment** - .env file protection for API keys and secrets
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

# Setup environment variables (Required for Supabase authentication)
copy .env.example .env
# Edit .env file with your Supabase credentials:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_ANON_KEY=your-anon-key
# SUPABASE_SERVICE_KEY=your-service-key

# Install Python dependencies
pip install -r requirements.txt

# Start the application (automatically loads .env and starts both services)
.\start-services.ps1
```

The application will be available at:
- **Web Application**: http://localhost:8082
- **Python ML API**: http://localhost:8083/health

### Stopping Services

```powershell
.\stop-services.ps1
```

## 🔐 Supabase Authentication Setup

RhythmIQ uses Supabase for secure user authentication. To set up:

1. **Create a Supabase account** at [https://supabase.com](https://supabase.com)
2. **Create a new project** (choose a strong database password)
3. **Get your API credentials** from Project Settings → API:
   - Project URL (e.g., `https://yourproject.supabase.co`)
   - `anon` public key (safe for client-side use)
   - `service_role` key (keep this secret!)

4. **Configure environment variables** by creating a `.env` file:
   ```properties
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-public-key-here
   SUPABASE_SERVICE_KEY=your-service-role-key-here
   ```

5. **Enable Email Authentication** in Supabase Dashboard:
   - Go to Authentication → Providers
   - Enable "Email" provider
   - Configure email templates (optional)

**Security Note**: Never commit your `.env` file to version control! It's already included in `.gitignore`.

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
│   │       │   ├── login.html       # Consistent theme login
│   │       │   ├── register.html    # Consistent theme registration
│   │       │   ├── dashboard.html   # Main dashboard
│   │       │   └── ...              # Other pages
│   │       ├── static/css/          # Stylesheets
│   │       └── application.properties # Spring Boot config
│   ├── pom.xml                      # Maven dependencies (Supabase, JWT)
│   └── target/                      # Built JAR (rhythmiq-webapp-1.0.0.jar)
├── 🧪 07_tests/                    # Python & PowerShell test scripts
│   ├── test_ecg_preprocessor.py     # Unit tests
│   └── test_all_classes.ps1         # Integration tests
├── 🚀 08_deployment/               # Deployment scripts & configs
│   ├── start-services.ps1           # Quick start (auto-loads .env)
│   ├── stop-services.ps1            # Stop all services
│   ├── load-env.ps1                 # Load environment variables
│   └── start-full-system.bat        # Windows batch starter
├── 🐍 09_python_api/               # Flask ML API (Port 8083)
│   ├── rhythmiq_api.py              # Main API server (with .env support)
│   └── requirements.txt             # Python dependencies (includes python-dotenv)
├── .env                             # Environment variables (SECRET - not in git)
├── .env.example                     # Template for .env setup
├── .gitignore                       # Git ignore rules (includes .env)
├── requirements.txt                 # Main Python dependencies
├── requirements-api.txt             # API-specific dependencies
├── render.yaml                      # Cloud deployment config
└── README.md                        # This file
```

## 🎨 Technology Stack

### Frontend
- **Framework**: Spring Boot 3.4.1 + Thymeleaf
- **Styling**: Custom CSS with Stormy/Cloud/Sunset/Evening palette
- **Typography**: Inter font family (Google Fonts)
- **Features**: Responsive design, dark mode, drag-and-drop upload
- **Theme Colors**: 
  - Stormy: `#98566D`
  - Evening: `#49466B`
  - Cloud: `#98878F`
  - Sunset: `#F5F3F4`

### Backend Services
- **Web Server**: Spring Boot (Java 21) - Port 8082
- **ML API**: Flask (Python 3.13) - Port 8083
- **Authentication**: Supabase (JWT-based)
- **Dependencies**: Apache HttpClient 5.3, Gson 2.10.1, Spring Security, JWT 0.12.3
- **ML Model**: RandomForest Classifier - 100% accuracy

### Machine Learning
- **Algorithm**: Random Forest
- **Features**: Image preprocessing, data augmentation
- **Classes**: 6 ECG rhythm types (F, M, N, Q, S, V)
- **Training Data**: 300 images (50 per class)
- **Test Data**: 30 images (5 per class)
- **Accuracy**: 100% on test dataset

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Overall Accuracy | 100% |
| Training Images | 300 (50 per class) |
| Test Images | 30 (5 per class) |
| Model Type | RandomForest |
| Model Size | 203 KB |
| Classes | 6 (F, M, N, Q, S, V) |
| Training Time | ~2-3 minutes |

## 🌐 Web Pages

All pages feature consistent Stormy/Cloud/Sunset/Evening theme with Inter font:

- **Login** (`/login`) - Modern authentication page with features showcase
- **Register** (`/register`) - User registration with medical disclaimer
- **Home** (`/`) - Professional landing page with hero section
- **Dashboard** (`/dashboard`) - Quick stats and action cards
- **Analyze ECG** (`/upload`) - Upload and analyze ECG images
- **Results** (`/results`) - Detailed analysis results with severity indicators
- **ECG Guide** (`/ecg-guide`) - Educational content about 6 rhythm types
- **About** (`/about`) - Company information and mission

### Theme Features
- **Gradient backgrounds**: Linear gradients using primary colors
- **Rounded corners**: 10-20px border radius for modern look
- **Hover effects**: Smooth transitions and elevation on interactions
- **Responsive**: Mobile-first design with breakpoints at 768px
- **Accessibility**: Proper contrast ratios and semantic HTML

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

# Test all ECG classes
.\07_tests\test_all_classes.ps1

# Test integration
.\07_tests\test_integration.ps1
```

## 🚀 Deployment

### Deploy to Render.com (Recommended)

1. **Push code to GitHub** (ensure `.env` is NOT pushed)
2. **Create Render account** at https://render.com
3. **Add environment variables** in Render Dashboard:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_KEY`
4. **Create new "Blueprint"** and connect GitHub repository
5. Render will automatically detect `render.yaml` and deploy both services

### Deploy to Railway.app

```powershell
npm i -g @railway/cli
railway login
railway init
# Add environment variables via Railway Dashboard
railway up
```

### Environment Variables for Production

When deploying, configure these environment variables:

```properties
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

**Security**: Never include your `.env` file in Docker images or Git commits!

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

**Made with ❤️ by Yash Raj**

</div>
