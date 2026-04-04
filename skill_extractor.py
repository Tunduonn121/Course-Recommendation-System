import json
# Sử dụng thư viện thế hệ mới của Google
from google import genai

def extract_skills_from_jd(jd_text, api_key):
    """
    Sử dụng Gemini API (thư viện genai mới) để trích xuất kỹ năng chuyên môn từ JD.
    Loại bỏ các công cụ (Git, VS Code...) và trả về định dạng JSON thuần.
    """
    try:
        # 1. Khởi tạo Client bằng thư viện mới
        client = genai.Client(api_key=api_key)
        
        # 2. Đóng gói System Prompt
        prompt = f"""Bạn là một Chuyên gia Nhân sự (HR) cấp cao trong lĩnh vực IT. Nhiệm vụ của bạn là đọc đoạn Mô tả công việc (Job Description) và trích xuất danh sách các kỹ năng chuyên môn lõi.

QUY TẮC:
1. CHỈ trích xuất Ngôn ngữ lập trình, Framework, Khái niệm Khoa học Máy tính (VD: Java, OOP, Spring Boot, Data Structures).
2. BỎ QUA HOÀN TOÀN các công cụ phần mềm (IDE, Tool) như: Git, GitHub, VS Code, Eclipse, Jira, Slack.
3. Gán Level cho từng kỹ năng: 1 (Beginner/Biết cơ bản), 2 (Intermediate/Có kinh nghiệm), 3 (Advanced/Senior/Thành thạo).

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:
Trả về DUY NHẤT một chuỗi JSON hợp lệ theo format sau, không có markdown (```json...```), không có bất kỳ lời chào hay giải thích nào:
{{
  "OOP": 3,
  "Java": 3,
  "Spring Boot": 3,
  "Docker": 1
}}

Văn bản JD cần phân tích:
"{jd_text}"
"""
        
        # 3. Gọi API với cú pháp mới và Model đời mới nhất
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # 4. Parsing Data (Làm sạch chuỗi)
        raw_text = response.text
        cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()
        skills_dict = json.loads(cleaned_text)
        
        return skills_dict

    except Exception as e:
        print(f"❌ LỖI TRONG QUÁ TRÌNH GỌI API: {e}")
        return {}

# --- TEST CASE ---
if __name__ == "__main__":
    MY_API_KEY = "AIzaSyDeYoN1b91H655vhN23fC-HBBe64jnQyuo" 
    
    test_jd = "Chúng tôi đang tìm kiếm Senior Backend Developer. Yêu cầu ứng viên có kiến thức nền tảng vững chắc về OOP và Data Structures. Bắt buộc thành thạo lập trình Java và có kinh nghiệm triển khai dự án thực tế với Spring Boot (ít nhất 2 năm). Quen thuộc với việc quản lý mã nguồn bằng Git và sử dụng VS Code. Biết cơ bản về Docker là một lợi thế lớn."
    
    print("⏳ Đang gửi yêu cầu cho Google Gemini phân tích JD...")
    
    result = extract_skills_from_jd(test_jd, MY_API_KEY)
    
    print("\n--- KẾT QUẢ TRÍCH XUẤT (TỪ LLM) ---")
    if result:
        print(f"Kiểu dữ liệu trả về: {type(result)}")
        print(json.dumps(result, indent=4, ensure_ascii=False))
        
        if "Git" not in result and "VS Code" not in result:
            print("\n✅ KIỂM TRA LUẬT: Pass! Đã loại bỏ thành công công cụ (Git, VS Code).")
        else:
            print("\n⚠️ KIỂM TRA LUẬT: Fail! AI vẫn giữ lại công cụ.")
    else:
        print("\nKhông trích xuất được dữ liệu.")