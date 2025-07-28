import fitz  # PyMuPDF
import json
import os
import glob
import pytesseract
from PIL import Image
from io import BytesIO
from collections import defaultdict

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_with_ocr(page):
    """Extract text from images in a PDF page using OCR"""
    text = ""
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = page.parent.extract_image(xref)
        image_bytes = base_image["image"]
        
        try:
            image = Image.open(BytesIO(image_bytes))
            # Perform OCR
            ocr_text = pytesseract.image_to_string(image)
            text += ocr_text + "\n"
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            continue
            
    return text.strip()

def extract_outline_structure(pdf_path):
    """Extract document structure with OCR support"""
    doc = fitz.open(pdf_path)
    text_blocks = []
    font_stats = defaultdict(int)
    
    for page in doc:
        page_number = page.number + 1
        
        text_page = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_DEHYPHENATE)
        
        for block in text_page.get("blocks", []):
            for line in block.get("lines", []):
                line_text = []
                line_size = None
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        line_text.append(text)
                        if line_size is None or span["size"] > line_size:
                            line_size = round(span["size"], 1)
                
                if line_text and line_size:
                    combined_text = ' '.join(line_text)
                    text_blocks.append({
                        "text": combined_text,
                        "size": line_size,
                        "page": page_number,
                        "bbox": line["bbox"],
                        "source": "text"
                    })

        ocr_text = extract_text_with_ocr(page)
        if ocr_text:
            for line in ocr_text.split('\n'):
                if line.strip():
                    text_blocks.append({
                        "text": line.strip(),
                        "size": 12, 
                        "page": page_number,
                        "bbox": (0, 0, 0, 0),  
                        "source": "ocr"
                    })

    doc.close()


    
    text_blocks.sort(key=lambda x: (-x["size"], x["bbox"][1]))
    
    # Identify title (largest text at the top)
    title = ""
    title_candidates = []
    min_title_size = max(b["size"] for b in text_blocks) * 0.8 if text_blocks else 0
    
    for block in text_blocks:
        if block["size"] >= min_title_size:
            title_candidates.append(block["text"])
        else:
            break
    
    title = " ".join(title_candidates) if title_candidates else (text_blocks[0]["text"] if text_blocks else "Untitled Document")
    
    # Process outline - group nearby text blocks with similar size
    outline = []
    processed_blocks = set()
    min_outline_size = max(b["size"] for b in text_blocks) * 0.4 if text_blocks else 0
    
    for i, block in enumerate(text_blocks):
        if i in processed_blocks or (text_blocks and block["size"] < min_outline_size):
            continue
            
        # Find nearby blocks to combine
        combined_text = block["text"]
        combined_size = block["size"]
        current_bbox = block["bbox"]
        
        for j, other_block in enumerate(text_blocks[i+1:], start=i+1):
            if j in processed_blocks:
                continue
                
            # Check if blocks are close vertically and have similar size
            vertical_dist = abs(other_block["bbox"][1] - current_bbox[1]) if current_bbox != (0,0,0,0) else float('inf')
            size_ratio = other_block["size"] / combined_size if combined_size > 0 else 1
            
            if vertical_dist < 50 and 0.8 <= size_ratio <= 1.2:
                combined_text += " " + other_block["text"]
                processed_blocks.add(j)
                # Update current bbox to the combined area
                if current_bbox != (0,0,0,0) and other_block["bbox"] != (0,0,0,0):
                    current_bbox = (
                        min(current_bbox[0], other_block["bbox"][0]),
                        min(current_bbox[1], other_block["bbox"][1]),
                        max(current_bbox[2], other_block["bbox"][2]),
                        max(current_bbox[3], other_block["bbox"][3])
                    )
        
        # Determine heading level based on size
        max_size = max(b["size"] for b in text_blocks) if text_blocks else 1
        size_ratio = block["size"] / max_size if max_size > 0 else 1
        
        if size_ratio > 0.7:
            level = "H1"
        elif size_ratio > 0.5:
            level = "H2"
        else:
            level = "H3"
        
        outline.append({
            "level": level,
            "text": combined_text,
            "page": block["page"],
            "source": block.get("source", "unknown")
        })

    # Clean up results
    def is_valid_outline_item(text):
        text = text.strip()
        return (len(text) > 2 and 
                not text.startswith('-') and 
                not all(c in '-=*' for c in text))
    
    cleaned_outline = [item for item in outline if is_valid_outline_item(item["text"])]
    
    return {
        "title": title.strip(),
        "outline": cleaned_outline
    }

def save_json(data, filename):
    """Save data to JSON file with UTF-8 encoding"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def process_pdf_to_outline(pdf_path, output_path):
    """Process a single PDF file and save the outline"""
    try:
        data = extract_outline_structure(pdf_path)
        save_json(data, output_path)
        filename = os.path.basename(pdf_path)
        output_filename = os.path.basename(output_path)
        print(f"✓ Processed {filename} -> {output_filename}")
        print(f"  Title: {data['title']}")
        print(f"  Outline items: {len(data['outline'])}")
        return True
    except Exception as e:
        print(f"Error processing {os.path.basename(pdf_path)}: {str(e)}")
        return False


def process_all_pdfs():
    if os.path.exists("/app/input"):
        input_dir = "/app/input"
        output_dir = "/app/output"
    else:
        input_dir = os.path.join("sample_dataset", "pdfs")
        output_dir = os.path.join("sample_dataset", "outputs")
    
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir} directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print("=" * 50)
    
    success_count = 0
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = os.path.join(output_dir, f"{name_without_ext}_outline.json")
        
        if process_pdf_to_outline(pdf_path, output_filename):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"Processing complete! Success: {success_count}/{len(pdf_files)}")

if __name__ == "__main__":
    process_all_pdfs()