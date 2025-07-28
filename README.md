# Challenge 1a(PDF Processor)

A Docker-based solution that extracts structured outlines from PDF documents, including:
- Regular PDF text through PyMuPDF
- Text embedded in images via Tesseract OCR
- Automatic hierarchy detection using font analysis
- Batch processing with clean JSON output

## 🌟 Key Features
| Feature | Description |
|---------|-------------|
| **Dual Text Extraction** | Combines native PDF text and OCR from images |
| **Smart Hierarchy Detection** | Identifies titles/H1-H3 headings by font analysis |
| **Multi-Language OCR** | Supports 100+ languages via Tesseract |
| **Batch Processing** | Processes entire directories of PDFs |
| **Docker Container** | Isolated, reproducible environment |
| **Structured JSON Output** | Consistent format for easy integration |

## 🛠️ System Requirements
- **Docker** (Desktop or Engine)
- **Minimum Resources**:
  - 2 CPU cores
  - 4GB RAM (8GB recommended for OCR)
  - 1GB disk space
    
## 🏗️ Project Structure

```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # Generated JSON outline files
│   └── pdfs/           # Input PDF files
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── process_pdfs.py    # Main processing script
└── README.md          # Project documentation
```

## 🔧 Installation & Setup

### 1. Clone or Download the Project
```bash
git clone https://github.com/Bisu7/Challenge_1a
cd Challenge_1a
```

### 2. Prepare Your PDF Files
Place your PDF files in the `sample_dataset/pdfs/` directory:
```bash
# Create directories if they don't exist
mkdir -p sample_dataset/pdfs
mkdir -p sample_dataset/outputs

# Copy your PDF files
cp your-document.pdf sample_dataset/pdfs/
```

### 3. Build the Docker Image
```bash
docker build --platform linux/amd64 -t pdf-processor .
```

---




## 🚀 Usage

### Docker Execution (Recommended)

**Linux/Mac:**
```bash
docker run --rm \
  -v "$(pwd)/sample_dataset/pdfs:/app/input:ro" \
  -v "$(pwd)/sample_dataset/outputs:/app/output" \
  --network none \
  pdf-processor
```

**Windows PowerShell:**
```powershell
docker run --rm -v "${PWD}/sample_dataset/pdfs:/app/input:ro" -v "${PWD}/sample_dataset/outputs:/app/output" --network none pdf-processor
```

**Windows Command Prompt:**
```cmd
docker run --rm -v "%cd%\sample_dataset\pdfs:/app/input:ro" -v "%cd%\sample_dataset\outputs:/app/output" --network none pdf-processor
```

### Local Development (Optional)
For testing and development:
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python process_pdfs.py
```

## 📊 Output Format

The tool generates JSON files with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "1.1 Overview",
      "page": 2
    },
    {
      "level": "H3",
      "text": "1.1.1 Background",
      "page": 3
    }
  ]
}
```

### Field Descriptions
- **title**: The main document title (largest font size, typically on first pages)
- **outline**: Array of hierarchical headings
  - **level**: Heading level (`H1`, `H2`, `H3`)
  - **text**: The actual heading text
  - **page**: Page number where the heading appears

## 🔧 How It Works

### ⚙️ Processing Pipeline

#### 🗂️ Text Extraction
- Extract **native text** using `PyMuPDF` (for text-based PDFs)
- Use **Tesseract OCR** for scanned/image-based PDFs
- Preserve **font metadata** (size, font name, boldness)

#### 🧱 Structure Analysis
- Detect headings using **font size ranking**:
  - Largest → `Title`, next → `H1`, `H2`, `H3`, etc.
- Group related text using **spatial layout**
- Track and record **page numbers** for each section

#### 📤 Output Generation
- Export results in a **validated JSON format**
- Encode output using **UTF-8**
- Implement robust **error logging** for traceability

## 🛠️ Technical Details

### Core Dependencies
- **PyMuPDF (fitz)**: PDF processing and text extraction
- **Python 3.9**: Runtime environment
- **json**: Output formatting
- **os/glob**: File system operations

### Docker Configuration
- **Base Image**: `python:3.9-slim`
- **Platform**: `linux/amd64` for cross-platform compatibility
- **Network**: Isolated (`--network none`) for security
- **Volumes**: Read-only input, writable output

### Performance Considerations
- Processes documents page by page for memory efficiency
- Handles large documents without loading entire content into memory
- Graceful error handling prevents single file failures from stopping batch processing

## 📝 Example Usage

### Input Files
```
sample_dataset/pdfs/
├── file01.pdf
├── file02.pdf
└── file03.pdf
```

### Running the Container
```bash
docker run --rm -v "${PWD}/sample_dataset/pdfs:/app/input:ro" -v "${PWD}/sample_dataset/outputs:/app/output" --network none pdf-processor
```

## 🔧 Troubleshooting

### Common Issues

**No PDF files found:**
- Ensure PDF files are in `sample_dataset/pdfs/`
- Check file permissions and extensions

**Docker build fails:**
- Ensure Docker is running
- Check internet connection for dependency downloads

**Empty outline output:**
- Document may have unusual font structure
- Check if PDF contains extractable text (not just images)

**Permission errors:**
- Ensure output directory exists and is writable
- On Linux, check directory ownership

