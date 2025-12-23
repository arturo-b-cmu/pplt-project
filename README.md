# Privacy-First RAG System: Security Research on Prompt Injection Vulnerabilities

A Retrieval Augmented Generation (RAG) system built with Llama 3, Flask, and ChromaDB for researching indirect prompt injection vulnerabilities in medical AI applications. This project demonstrates privacy protection mechanisms and quantifies security risks in LLM-powered document query systems.

## 🎯 Research Focus

This implementation explores:
- Indirect prompt injection attack vectors in RAG systems
- Privacy protection through system-level prompts
- HIPAA compliance violations via contextual integrity framework
- Comparative analysis of direct vs. indirect injection effectiveness

## 🔧 Tech Stack

- **LLM**: Llama 3 (via Ollama)
- **Framework**: Flask API
- **Vector Database**: ChromaDB
- **Embeddings**: FastEmbed
- **Document Processing**: PDFPlumber, CSV support
- **Security**: Privacy-focused system prompts with PII protection

## 📋 Prerequisites

1. **Install Ollama**: [ollama.com](https://ollama.com)
2. **Pull Llama 3 model**:
```bash
   ollama pull llama3
```
3. **Start Ollama server**:
```bash
   ollama serve
```

## 🚀 Installation

### 1. Clone Repository
```bash
git clone #edit this with new name
cd rag
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Required Directories
```bash
mkdir pdf db
```

### 5. Run Application
```bash
python3 app.py
```

The app will run at `http://127.0.0.1:8081`

## 📡 API Endpoints

### 1. Document Upload
Upload PDF or CSV documents for processing and embedding.

**Endpoint:** `POST /pdf`

**Request:**
```bash
curl -X POST http://127.0.0.1:8081/pdf \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "status": "Successfully Uploaded",
  "filename": "document.pdf",
  "doc_len": 25,
  "chunks": 150
}
```

### 2. Query Documents
Ask questions about uploaded documents with privacy-first responses.

**Endpoint:** `POST /ask_pdf`

**Request:**
```bash
curl -X POST http://127.0.0.1:8081/ask_pdf \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```

**Response:**
```json
{
  "answer": "This document contains information about..."
}
```

### 3. System Status
Check uploaded files and database status.

**Endpoint:** `GET /status`

**Request:**
```bash
curl http://127.0.0.1:8081/status
```

**Response:**
```json
{
  "uploaded_files": ["document.pdf", "data.csv"],
  "file_count": 2,
  "total_chunks_in_db": 305
}
```

### 4. General AI Query (No Document Context)
Direct queries to Llama 3 without RAG.

**Endpoint:** `POST /ai`

**Request:**
```bash
curl -X POST http://127.0.0.1:8081/ai \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me a joke"}'
```

**Response:**
```json
{
  "answer": "Why did the AI go to therapy?..."
}
```

## 🔒 Privacy Features

### System Prompt Protection
The application includes a privacy-focused system prompt that:
- Prohibits disclosure of personally identifiable information (PII)
- Defines protected HIPAA identifiers (names, DOB, MRN, etc.)
- Provides aggregated summaries without revealing identities
- Implements jailbreak protection mechanisms

### Protected Information Types
- Names, addresses, phone numbers
- Social Security Numbers, Medical Record Numbers
- Dates of birth, insurance IDs
- Medical diagnoses, prescriptions
- Email addresses, account numbers

## 🧪 Security Testing

This system was used to evaluate prompt injection vulnerabilities:

### Research Findings
- **Attack Success Rate**: 47.4% for indirect injection vs. 29.4% for direct
- **PII Disclosure**: 100% of successful attacks leaked patient identifiers
- **HIPAA Violations**: Quantified through contextual integrity framework
- **Total Test Queries**: 45 (36 attacks, 9 benign)

### Test Methodology
1. Upload documents with embedded malicious prompts
2. Execute benign administrative queries
3. Measure PII disclosure rates and types
4. Calculate contextual integrity violation scores

## 📊 Project Structure
```
rag/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── pdf/                   # Uploaded documents storage
├── db/                    # ChromaDB vector database
└── README.md             # This file
```

## 🛠️ Configuration

### Modify System Prompt
Edit the `raw_prompt` variable in `app.py` to customize privacy rules:
```python
raw_prompt = PromptTemplate.from_template(
    """
    <s>[INST] You are a privacy-focused assistant...
    [Your custom instructions here]
    [/INST] </s>
    """
)
```

### Adjust Server Settings
Modify `start_app()` function in `app.py`:
```python
def start_app():
    app.run(host="0.0.0.0", port=8081, debug=True)
```

### Configure Ollama Connection
To use a remote Ollama instance:
```python
cached_llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)
```

## 🧹 Clearing Data

### Clear Vector Database Only
```bash
rm -rf db/
mkdir db
```

### Clear Everything (Full Reset)
```bash
rm -rf db/ pdf/*
mkdir db
```

## ⚠️ Known Limitations

- System prompt protections can be bypassed via indirect injection
- Patient identifiers (names, IDs) are most vulnerable to disclosure
- Clinical notes show higher resistance to extraction
- No authentication/authorization mechanisms (research prototype)

## 📚 Research Applications

This system has been used to study:
- Contextual integrity violations in medical AI
- HIPAA compliance in LLM-powered applications  
- Indirect vs. direct prompt injection effectiveness
- Privacy-preserving RAG architectures

## 🔗 Related Resources

- [Ollama Documentation](https://ollama.com)
- [LangChain Security](https://python.langchain.com/docs/security)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [HEW FIPPs Principles](https://www.hhs.gov/foia/privacy/index.html)


## 👤 Authors

- Arturo Bohuchot
- Chloe Cowan
- Jack Lenga
- Samhitha Duggirala

Carnegie Mellon University  


## 🙏 Acknowledgments

Built for security research and educational purposes. This project demonstrates vulnerabilities in LLM-based systems and should be used responsibly for improving AI safety and privacy protections.

---

**⚠️ Disclaimer**: This is a research prototype demonstrating security vulnerabilities. Not intended for production use with real patient data without proper security hardening, authentication, and compliance measures.