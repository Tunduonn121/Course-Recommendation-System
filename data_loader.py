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

def build_course_tree(flat_courses_list):
    """
    Hàm này nhận vào một danh sách phẳng các khóa học
    và gom nhóm chúng lại thành cấu trúc Cây (Dictionary lồng nhau).
    """
    course_tree = {} # Khởi tạo Cây rỗng (Root Node)

    for course in flat_courses_list:
        # Lấy thông tin danh mục của khóa học hiện tại
        cat = course['category']       # Ví dụ: "Backend", "DevOps"
        subcat = course['subcategory'] # Ví dụ: "Java", "Python"

        # 1. Nếu Danh mục lớn (Category) chưa có trong Cây -> Tạo mới
        if cat not in course_tree:
            course_tree[cat] = {}

        # 2. Nếu Danh mục con (Subcategory) chưa có trong Danh mục lớn -> Tạo mới dạng List (Nút Lá)
        if subcat not in course_tree[cat]:
            course_tree[cat][subcat] = []

        # 3. Thêm khóa học vào đúng vị trí Nút Lá (Leaf Node)
        course_tree[cat][subcat].append(course)

    return course_tree

# --- Phần này chỉ để test xem hàm có chạy đúng không ---
if __name__ == "__main__":
    # Tên file JSON bạn vừa tạo
    my_file = "mock_courses.json"
    
    # Gọi hàm để đọc
    courses = load_mock_courses(my_file)
    
"""
    print ("Truy xuất toàn bộ khóa học:\n")
    for index,course in enumerate (courses):
        print (f"khoa hoc thu {index+1}")
        print (f"ten khoa:{course['title']}")
        print (f"ky nang:{course['target_skill']}")
        print (f"cap do:{course['level']}")
"""

"""
    print ("Truy xuất toàn bộ khóa học:\n")
    for index,course in enumerate (courses):
        print (f"khoa hoc thu {index+1}")
        print (f"ten khoa:{course['title']}")
        print (f"ky nang:{course['target_skill']}")
        print (f"cap do:{course['level']}")
"""
"""
    print ("Truy xuất toàn bộ khóa học:\n")
    for index,course in enumerate (courses):
        print (f"khoa hoc thu {index+1}")
        print (f"ten khoa:{course['title']}")
        print (f"ky nang:{course['target_skill']}")
        print (f"cap do:{course['level']}")
"""
"""
    print ("Truy xuất toàn bộ khóa học:\n")
    for index,course in enumerate (courses):
        print (f"khoa hoc thu {index+1}")
        print (f"ten khoa:{course['title']}")
        print (f"ky nang:{course['target_skill']}")
        print (f"cap do:{course['level']}")
"""
"""
    print ("Truy xuất toàn bộ khóa học:\n")
    for index,course in enumerate (courses):
        print (f"khoa hoc thu {index+1}")
        print (f"ten khoa:{course['title']}")
        print (f"ky nang:{course['target_skill']}")
        print (f"cap do:{course['level']}")
"""