# LegalLens - AI-Powered Contract Risk Analyzer

LegalLens is an advanced AI-powered web application that analyzes legal contracts for risks, identifies potential issues, and provides intelligent recommendations for improvement. Built with cutting-edge Generative AI technologies, it offers comprehensive contract analysis through a modern, responsive web interface.

## 🚀 Features

- **AI-Powered Risk Analysis**: Utilizes NVIDIA Nemotron models for advanced legal document analysis
- **Document Processing**: Supports PDF and text file uploads with automatic text extraction
- **Intelligent Contract Rewriting**: AI-generated improvements for clarity and fairness
- **Real-time Analysis**: Fast, responsive analysis with detailed risk scoring
- **Modern Web Interface**: Clean, intuitive UI built with Next.js and Tailwind CSS
- **Responsive Design**: Works seamlessly across desktop and mobile devices

## 🤖 AI Technologies

### Core Generative AI Models
- **NVIDIA Nemotron-49B**: Advanced legal risk analysis and contract evaluation
- **NVIDIA Nemotron-9B**: Contract rewriting and improvement generation
- **NVIDIA Nemoretriever-300M**: Semantic embeddings for intelligent document retrieval

### AI/ML Libraries
- **FAISS**: Vector similarity search for semantic retrieval
- **BM25**: Keyword-based information retrieval
- **Hybrid Search**: Combined semantic + keyword search architecture
- **MMR (Maximal Marginal Relevance)**: Search result diversification
- **JSON-based AI Output**: Structured prompt engineering for consistent responses

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: High-performance async Python API
- **Python**: Core backend language
- **Uvicorn**: ASGI server for production deployment
- **pdfplumber**: PDF text extraction
- **python-multipart**: File upload handling

### Frontend (Next.js)
- **Next.js**: Full-stack React framework
- **React**: Component-based UI development
- **TypeScript**: Type-safe frontend development
- **Tailwind CSS**: Utility-first styling framework
- **Axios**: HTTP client for API communication

## 📁 Project Structure

```
LegalLens/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   └── config.py          # Configuration
│   │   ├── services/
│   │   │   └── analyzer.py        # AI analysis logic
│   │   └── main.py                # FastAPI application
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Main React component
│   │   └── globals.css            # Global styles
│   ├── tailwind.config.js         # Tailwind configuration
│   └── package.json               # Node.js dependencies
├── start_backend.py               # Backend startup script
├── start_frontend.py              # Frontend startup script
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- NVIDIA API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harthikss9/LegalLens.git
   cd LegalLens
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure environment variables**
   ```bash
   export NVIDIA_API_KEY="your_nvidia_api_key_here"
   ```

5. **Start the application**
   ```bash
   # Terminal 1 - Start backend
   python3 start_backend.py
   
   # Terminal 2 - Start frontend
   python3 start_frontend.py
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8001

## 🔧 Usage

1. **Upload a Contract**: Drag and drop or click to upload a PDF or text file
2. **Analyze**: Click "Analyze Contract" to start the AI analysis
3. **Review Results**: View detailed risk analysis, issues found, and recommendations
4. **Download Improved Contract**: Get the AI-rewritten version with improvements

## 🎯 Key Features

### Risk Analysis
- Identifies risky, unclear, and safe clauses
- Provides detailed risk scoring (0-100)
- Categorizes issues by severity and type
- Offers specific recommendations for improvement

### Contract Improvement
- AI-generated contract rewrites
- Maintains original intent while improving clarity
- Addresses identified risks and issues
- Provides summary of changes made

### Modern UI/UX
- Clean, professional interface
- Responsive design for all devices
- Real-time progress indicators
- Intuitive file upload and analysis workflow

## 🛠️ Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 📊 API Endpoints

- `POST /api/extract` - Extract text from uploaded document
- `POST /api/analyze` - Analyze document for risks and improvements

## 🔒 Security

- Secure API key management
- Input validation and sanitization
- File type restrictions (PDF, TXT only)
- Error handling and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NVIDIA for providing access to their advanced AI models
- The open-source community for the amazing tools and libraries
- Legal professionals who provided feedback and requirements

## 📞 Contact

For questions, suggestions, or collaboration opportunities, please open an issue or contact the maintainers.

---

**LegalLens** - Making legal contract analysis accessible through AI technology.