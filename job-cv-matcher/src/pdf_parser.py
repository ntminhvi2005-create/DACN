"""
Module trích xuất văn bản từ file PDF
So sánh và sử dụng pdfplumber (chọn vì độ chính xác cao hơn với CV phức tạp)
"""

import pdfplumber
import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_pdfplumber(pdf_path: str) -> Tuple[str, bool]:
    """
    Trích xuất text từ PDF bằng pdfplumber
    
    Args:
        pdf_path: Đường dẫn đến file PDF
        
    Returns:
        Tuple[str, bool]: (text, success_flag)
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Kiểm tra nếu text quá ngắn (có thể là PDF scan)
        if len(text.strip()) < 50:
            return "", False
        
        return text.strip(), True
    
    except Exception as e:
        logger.error(f"Lỗi khi đọc file {pdf_path}: {str(e)}")
        return "", False


def extract_text_pymupdf(pdf_path: str) -> Tuple[str, bool]:
    """
    Trích xuất text từ PDF bằng PyMuPDF (fitz)
    
    Args:
        pdf_path: Đường dẫn đến file PDF
        
    Returns:
        Tuple[str, bool]: (text, success_flag)
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
        
        doc.close()
        
        # Kiểm tra nếu text quá ngắn
        if len(text.strip()) < 50:
            return "", False
        
        return text.strip(), True
    
    except Exception as e:
        logger.error(f"Lỗi khi đọc file {pdf_path}: {str(e)}")
        return "", False


def compare_extraction_methods(pdf_path: str) -> dict:
    """
    So sánh 2 phương pháp trích xuất trên cùng 1 file PDF
    
    Returns:
        Dictionary chứa kết quả so sánh
    """
    import time
    
    # Test pdfplumber
    start = time.time()
    text_plumber, success_plumber = extract_text_pdfplumber(pdf_path)
    time_plumber = time.time() - start
    
    # Test PyMuPDF
    start = time.time()
    text_pymupdf, success_pymupdf = extract_text_pymupdf(pdf_path)
    time_pymupdf = time.time() - start
    
    return {
        'pdfplumber': {
            'text_length': len(text_plumber),
            'success': success_plumber,
            'time': time_plumber,
            'preview': text_plumber[:200] if text_plumber else ""
        },
        'pymupdf': {
            'text_length': len(text_pymupdf),
            'success': success_pymupdf,
            'time': time_pymupdf,
            'preview': text_pymupdf[:200] if text_pymupdf else ""
        }
    }


if __name__ == "__main__":
    # Test nhanh với 1 file PDF mẫu
    test_pdf = "data/raw/sample_cv.pdf"
    if Path(test_pdf).exists():
        result = compare_extraction_methods(test_pdf)
        print("=== KẾT QUẢ SO SÁNH ===")
        print(f"pdfplumber: {result['pdfplumber']['text_length']} ký tự, {result['pdfplumber']['time']:.3f}s")
        print(f"PyMuPDF: {result['pymupdf']['text_length']} ký tự, {result['pymupdf']['time']:.3f}s")
    else:
        print(f"Không tìm thấy file test: {test_pdf}")