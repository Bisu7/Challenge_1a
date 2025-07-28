import fitz  # PyMuPDF
import json
import os
import glob

def extract_outline_structure(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page in doc:
        page_number = page.number + 1  # human-readable page number
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        blocks.append({
                            "text": text,
                            "size": round(span["size"], 1),
                            "font": span["font"],
                            "bold": "Bold" in span["font"],
                            "page": page_number
                        })

    doc.close()  # Close the document

    # Step 1: Determine unique sizes and classify as Title, H1, H2, ...
    unique_sizes = sorted(set(b["size"] for b in blocks), reverse=True)
    size_to_level = {}
    for idx, size in enumerate(unique_sizes):
        if idx == 0:
            size_to_level[size] = "title"
        elif idx == 1:
            size_to_level[size] = "H1"
        elif idx == 2:
            size_to_level[size] = "H2"
        elif idx == 3:
            size_to_level[size] = "H3"
        else:
            size_to_level[size] = "Body"

    # Step 2: Extract title and outline
    title = ""
    outline = []

    for block in blocks:
        level = size_to_level.get(block["size"], "Body")
        text = block["text"]
        page = block["page"]

        if level == "title" and not title:
            title = text

        if level in ["H1", "H2", "H3"]:
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    return {"title": title, "outline": outline}

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def process_pdf_to_outline(pdf_path, output_path):
    data = extract_outline_structure(pdf_path)
    save_json(data, output_path)
    filename = os.path.basename(pdf_path)
    output_filename = os.path.basename(output_path)
    print(f"✓ Processed {filename} -> {output_filename}")
    print(f"  Title: {data['title']}")
    print(f"  Outline items: {len(data['outline'])}")

def process_all_pdfs():
    """Process all PDFs in the input directory"""
    # Check if running in Docker or locally
    if os.path.exists("/app/input"):
        # Docker environment
        input_dir = "/app/input"
        output_dir = "/app/output"
    else:
        # Local development environment
        input_dir = "./sample_dataset/pdfs"
        output_dir = "./sample_dataset/outputs"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files in input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir} directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print("=" * 50)
    
    for pdf_path in pdf_files:
        try:
            # Get filename without extension
            filename = os.path.basename(pdf_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            # Create output filename
            output_filename = os.path.join(output_dir, f"{name_without_ext}_outline.json")
            
            # Process the PDF
            process_pdf_to_outline(pdf_path, output_filename)
            print()
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    print("=" * 50)
    print("Processing complete!")

# Example usage
if __name__ == "__main__":
    # For Docker environment - process all PDFs
    process_all_pdfs()