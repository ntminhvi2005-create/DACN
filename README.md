# Job-Candidate Matching System

Hệ thống gợi ý và đánh giá phù hợp Ứng viên - Công việc dựa trên So sánh Ngữ nghĩa và Tư vấn Cải thiện Hồ sơ.

## Mô tả

Đồ án chuyên ngành xây dựng hệ thống AI giúp:
- **Nhà tuyển dụng:** Tìm kiếm và xếp hạng CV ứng viên phù hợp với JD nhanh chóng
- **Ứng viên:** Nhận đánh giá "CV Health Check" và lời khuyên cải thiện hồ sơ

## Công nghệ

- **NLP:** Sentence-BERT, spaCy
- **Tìm kiếm vector:** FAISS
- **Backend:** FastAPI
- **Frontend:** Streamlit

## Cấu trúc dự án
job-cv-matcher/
├── data/ # Dữ liệu
├── notebooks/ # Jupyter notebooks cho EDA và thử nghiệm
├── src/ # Mã nguồn chính
├── app/ # FastAPI và Streamlit
└── requirements.txt

## Cài đặt

```bash
pip install -r requirements.txt