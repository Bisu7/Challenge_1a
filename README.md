# Challenge 1a(PDF Processor)

A robust Docker-based solution for extracting hierarchical outline structures from PDF documents using PyMuPDF. This tool automatically analyzes font sizes and formats to identify document titles and multi-level headings, outputting structured JSON files suitable for document navigation and content analysis.

## 🚀 Features

- **Automatic Hierarchy Detection**: Intelligently identifies document structure based on font size analysis
- **Multi-level Headings**: Extracts titles, H1, H2, and H3 level headings with page references
- **Batch Processing**: Processes multiple PDF files in a single run
- **Docker Support**: Fully containerized solution with consistent cross-platform execution
- **JSON Output**: Clean, structured output format for easy integration
- **Error Resilience**: Continues processing even if individual files encounter issues

## 📋 Requirements

- **Docker**: Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- **Input**: PDF files to be processed
- **System**: Any system supporting Docker containers

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
git clone <your-repository-url>
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
docker build --platform linux/amd64 -t pdf-outline-extractor .
```

## 🚀 Usage

### Docker Execution (Recommended)

**Linux/Mac:**
```bash
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  pdf-outline-extractor
```

**Windows PowerShell:**
```powershell
docker run --rm `
  -v "${PWD}/sample_dataset/pdfs:/app/input:ro" `
  -v "${PWD}/sample_dataset/outputs:/app/output" `
  --network none `
  pdf-outline-extractor
```

**Windows Command Prompt:**
```cmd
docker run --rm ^
  -v "%cd%/sample_dataset/pdfs:/app/input:ro" ^
  -v "%cd%/sample_dataset/outputs:/app/output" ^
  --network none ^
  pdf-outline-extractor
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

## 🔍 How It Works

### 1. Text Extraction
- Opens PDF files using PyMuPDF (fitz)
- Extracts text with font metadata from every page
- Preserves font size, style, and positioning information

### 2. Font Analysis
- Analyzes all unique font sizes in the document
- Ranks sizes from largest to smallest
- Assigns hierarchy levels based on size ranking:
  - **Largest**: Document Title
  - **Second**: H1 headings
  - **Third**: H2 headings
  - **Fourth**: H3 headings
  - **Remaining**: Body text

### 3. Structure Extraction
- Identifies title from the largest font size (preferably on early pages)
- Extracts headings at H1, H2, and H3 levels
- Records page numbers for each heading
- Removes duplicate entries

### 4. JSON Generation
- Formats extracted data into structured JSON
- Saves output files with `_outline.json` suffix
- Ensures UTF-8 encoding for international character support

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
├── research_paper.pdf
├── technical_manual.pdf
└── book_chapter.pdf
```

### Running the Container
```bash
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  pdf-outline-extractor
```

### Generated Output
```
sample_dataset/outputs/
├── research_paper_outline.json
├── technical_manual_outline.json
└── book_chapter_outline.json
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

### Debug Mode
For detailed processing information, modify the script to include debug output or check container logs.

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample PDF files
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Docker and PyMuPDF documentation
3. Submit issues through the project repository

---

**Built with ❤️ using Python, PyMuPDF, and Docker**
