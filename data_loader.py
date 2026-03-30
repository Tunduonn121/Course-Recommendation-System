import json

def load_mock_courses(file_path):
    """
    Hàm này dùng để đọc file JSON và chuyển nó thành List/Dictionary trong Python.
    """
    try:
        # Mở file JSON với mã hóa utf-8 để không bị lỗi tiếng Việt
        with open(file_path, 'r', encoding='utf-8') as file:
            # Hàm json.load() sẽ tự động biến file JSON thành 1 List chứa các Dictionary
            courses_data = json.load(file)
            return courses_data
            
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_path}")
        return []
    except json.JSONDecodeError:
        print("Lỗi: File JSON bị sai định dạng!")
        return []

# --- Phần này chỉ để test xem hàm có chạy đúng không ---
if __name__ == "__main__":
    # Tên file JSON bạn vừa tạo
    my_file = "mock_courses.json"
    
    # Gọi hàm để đọc
    courses = load_mock_courses(my_file)
    
    # In thử ra màn hình xem có lấy được dữ liệu không
    print(f"Đã tải thành công {len(courses)} khóa học!\n")
    
    # In thử tên và kỹ năng của khóa học đầu tiên (Index 0)
    print("Thông tin khóa học đầu tiên:")
    print(f"- Tên khóa: {courses[0]['title']}")
    print(f"- Kỹ năng dạy: {courses[0]['target_skill']}")
    print(f"- Cấp độ (Level): {courses[0]['level']}")