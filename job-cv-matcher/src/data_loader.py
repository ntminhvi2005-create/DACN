"""
Module tải và lọc dữ liệu CV/JD theo thời gian (1-5 năm gần đây)
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_filter_data(
    csv_path: str,
    date_column: str = 'post_date',
    start_year: int = 2021,
    end_year: int = 2026
) -> pd.DataFrame:
    """
    Tải dữ liệu từ CSV và lọc theo khoảng thời gian
    
    Args:
        csv_path: Đường dẫn đến file CSV
        date_column: Tên cột chứa ngày tháng
        start_year: Năm bắt đầu (mặc định 2021)
        end_year: Năm kết thúc (mặc định 2026)
        
    Returns:
        DataFrame đã được lọc
    """
    logger.info(f"Đang tải dữ liệu từ {csv_path}...")
    df = pd.read_csv(csv_path)
    
    original_count = len(df)
    logger.info(f"Tổng số bản ghi ban đầu: {original_count}")
    
    # Kiểm tra cột ngày tháng có tồn tại không
    if date_column not in df.columns:
        logger.warning(f"Không tìm thấy cột '{date_column}'. Trả về toàn bộ dữ liệu.")
        return df
    
    # Chuyển đổi cột ngày tháng
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Lọc theo năm
    start_date = pd.to_datetime(f'{start_year}-01-01')
    end_date = pd.to_datetime(f'{end_year}-12-31')
    
    df_filtered = df[
        (df[date_column] >= start_date) & 
        (df[date_column] <= end_date)
    ].copy()
    
    filtered_count = len(df_filtered)
    logger.info(f"Số bản ghi sau khi lọc ({start_year}-{end_year}): {filtered_count}")
    logger.info(f"Tỷ lệ giữ lại: {filtered_count/original_count*100:.1f}%")
    
    return df_filtered


def validate_extracted_text(df: pd.DataFrame, text_column: str = 'description') -> pd.DataFrame:
    """
    Kiểm tra và loại bỏ các bản ghi có text quá ngắn (PDF lỗi/scan)
    
    Args:
        df: DataFrame chứa dữ liệu
        text_column: Tên cột chứa văn bản
        
    Returns:
        DataFrame đã được làm sạch
    """
    if text_column not in df.columns:
        logger.warning(f"Không tìm thấy cột '{text_column}'")
        return df
    
    original_count = len(df)
    
    # Loại bỏ các bản ghi có text < 50 ký tự
    df_clean = df[df[text_column].str.len() >= 50].copy()
    
    removed_count = original_count - len(df_clean)
    logger.info(f"Đã loại bỏ {removed_count} bản ghi có text quá ngắn (< 50 ký tự)")
    logger.info(f"Số bản ghi còn lại: {len(df_clean)}")
    
    return df_clean


if __name__ == "__main__":
    # Test nhanh
    test_csv = "data/raw/job_postings.csv"
    if Path(test_csv).exists():
        df = load_and_filter_data(test_csv, date_column='post_date')
        print(f"\nKích thước dữ liệu sau khi lọc: {df.shape}")
        print(df.head())
    else:
        print(f"Không tìm thấy file: {test_csv}")