import json
import os
import re
from google import genai
from dotenv import load_dotenv

def rank_courses_with_llm(candidate_courses, gap_dict, api_key, top_k=3):
    """
    Sử dụng Gemini để đánh giá và xếp hạng khóa học dựa trên LUẬT SƯ PHẠM nghiêm ngặt.
    Parsing JSON bọc thép: Kháng lại mọi ảo giác và giải thích thừa của AI.
    """
    try:
        # Khởi tạo Client
        client = genai.Client(api_key=api_key)
        
        candidates_str = json.dumps(candidate_courses, ensure_ascii=False, indent=2)
        gap_str = json.dumps(gap_dict, ensure_ascii=False)
        
        # System Prompt CẬP NHẬT: Thêm lệnh cấm giải thích thừa
        prompt = f"""Bạn là một Hệ thống Đề xuất Khóa học nghiêm ngặt.

THÔNG TIN ĐẦU VÀO:
- Skill Gap: {gap_str}
- Danh sách Khóa học Ứng viên: {candidates_str}

LUẬT SƯ PHẠM (QUAN TRỌNG NHẤT):
Bạn PHẢI đối chiếu level của khóa học với giá trị NHỎ NHẤT (cấp độ nền tảng) trong mảng Gap của từng kỹ năng.
Ví dụ: Nếu Gap là "Spring Boot": [1, 2], khóa học Level 2 KHÔNG được coi là hợp lệ lúc này vì học viên thiếu nền tảng Level 1.

TIÊU CHÍ CHẤM ĐIỂM (CHỈ CHỌN 1):
- (90-100 điểm): Khóa học lấp được CÙNG LÚC NHIỀU kỹ năng, VÀ level của khóa học khớp chính xác với cấp độ NHỎ NHẤT đang thiếu của các kỹ năng đó.
- (70-89 điểm): Khóa học lấp được 1 kỹ năng quan trọng, VÀ level của khóa học khớp chính xác với cấp độ NHỎ NHẤT đang thiếu của kỹ năng đó.
- (50-69 điểm): Khóa học có kỹ năng thuộc Gap, nhưng level của nó LỚN HƠN cấp độ nhỏ nhất đang thiếu.
- (Dưới 50 điểm): Khóa học có level nhỏ hơn toàn bộ mảng Gap, hoặc không chứa kỹ năng nào.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:
TUYỆT ĐỐI KHÔNG lặp lại đề bài. TUYỆT ĐỐI KHÔNG giải thích gì thêm ở bên ngoài.
Chỉ trả về DUY NHẤT một mảng JSON hợp lệ chứa tối đa {top_k} khóa học, cấu trúc bắt buộc:
[
  {{
    "course_id": "ID khóa học",
    "relevance_score": Điểm số,
    "reasoning": "Giải thích ngắn gọn."
  }}
]"""
        
        # Gọi API với model mới nhất
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        raw_text = response.text
        
        # --- BẮT ĐẦU ĐOẠN CẬP NHẬT: REGEX BỌC THÉP ---
        # Tìm một mảng bắt đầu bằng dấu ngoặc vuông [, bên trong chứa ngoặc nhọn { và kết thúc bằng ]
        match = re.search(r'\[\s*\{.*\}\s*\]', raw_text, re.DOTALL)
        
        if match:
            json_str = match.group(0)
            try:
                ranked_courses = json.loads(json_str)
                return ranked_courses
            except json.JSONDecodeError as je:
                print(f"❌ LỖI GIẢI MÃ JSON: {je}")
                print(f"--- CHUỖI BỊ LỖI ---\n{json_str}\n-------------------")
                return []
        else:
            print(f"⚠️ Lỗi Parsing: AI không trả về định dạng mảng Object. Nguyên văn: \n{raw_text}")
            return []
        # --- KẾT THÚC ĐOẠN CẬP NHẬT ---

    except Exception as e:
        print(f"❌ LỖI TRONG QUÁ TRÌNH GỌI API: {e}")
        return []

# --- TEST CASE TÍCH HỢP (CHẠY THỬ NGHIỆM) ---
if __name__ == "__main__":
    load_dotenv()
    MY_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not MY_API_KEY:
        print("❌ Lỗi: Hãy kiểm tra file .env để đảm bảo có GEMINI_API_KEY.")
        exit()
    
    test_gap = {
        'Java': [2, 3], 
        'Spring Boot': [1, 2]
    }
    
    test_candidates = [
        {
            "id": "C002",
            "title": "Cấu trúc dữ liệu Java",
            "target_skills": ["Java"],
            "level": 2,
            "description": "Dành cho người đã biết Java cơ bản."
        },
        {
            "id": "C003",
            "title": "Lập trình Spring Boot nâng cao",
            "target_skills": ["Java", "Spring Boot"],
            "level": 3,
            "description": "Khóa Senior chuyên sâu."
        },
        {
            "id": "C004", 
            "title": "Lập trình Spring Boot nâng cao",
            "target_skills": ["Java", "Spring Boot"],
            "level": 2,
            "description": "Khóa Senior chuyên sâu."
        },
        {
            "id": "C007", # Đổi ID để dễ nhìn
            "title": "Lập trình Spring Boot căn bản",
            "target_skills": ["Spring Boot"],
            "level": 1,
            "description": "Khóa nền tảng."
        },
        {
            "id": "C005", 
            "title": "Lập trình Spring Boot nâng cao",
            "target_skills": ["Spring Boot"],
            "level": 2,
            "description": "Khóa Senior chuyên sâu."
        },
        {
            "id": "C006", 
            "title": "Cấu trúc dữ liệu Java",
            "target_skills": ["Java"],
            "level": 3,
            "description": "Dành cho người đã biết Java cơ bản."
        }
    ]
    
    print("⏳ Đang gửi yêu cầu Ranking với LUẬT SƯ PHẠM NGHIÊM NGẶT (Bản chống ảo giác)...")
    
    ranked_result = rank_courses_with_llm(test_candidates, test_gap, MY_API_KEY, top_k=5)
    
    print("\n--- KẾT QUẢ XẾP HẠNG (RANKING) ---")
    if ranked_result:
        for idx, item in enumerate(ranked_result, 1):
            print(f"Hạng {idx} - ID: {item.get('course_id')}")
            print(f"  > Điểm số: {item.get('relevance_score')}/100")
            print(f"  > Lý do: {item.get('reasoning')}")
            print("-" * 50)
    else:
        print("Không có kết quả xếp hạng.")