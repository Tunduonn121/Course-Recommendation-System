import json
from data_loader import load_mock_courses, build_course_tree

def mock_llm_evaluate(node_name, gap_dict):
    """
    Giả lập AI đánh giá sự liên quan của một Node với khoảng trống kỹ năng.
    Hệ thống sẽ "cắt tỉa" nếu Node không liên quan đến kỹ năng cần học.
    """
    # Lấy danh sách các kỹ năng đang thiếu (Keys trong gap_dict)
    missing_skills = [skill.lower() for skill in gap_dict.keys()]
    node_name_lower = node_name.lower()
    
    # Logic giả lập: 
    # 1. Nếu tên Node khớp với kỹ năng thiếu (Java, Spring Boot...)
    # 2. Hoặc nếu Node là danh mục cha chứa kỹ năng đó (Backend)
    # Ở bản Mock, ta tạm thời cho phép "Backend" và "Computer Science" luôn True để test
    general_categories = ["backend", "computer science", "ai"]
    
    if any(skill in node_name_lower for skill in missing_skills):
        return True
    if node_name_lower in general_categories:
        return True
        
    return False

def dfs_tree_search(course_tree, gap_dict):
    """
    Thuật toán duyệt cây theo chiều sâu (DFS) sử dụng Stack.
    Tích hợp cơ chế Pruning (Cắt tỉa) dựa trên đánh giá của LLM.
    """
    stack = []
    candidate_courses = []

    # 1. Khởi tạo: Đẩy các Category tầng 1 vào stack
    # Cấu trúc của stack: mỗi phần tử là một tuple (tên_node, dữ liệu_node)
    for cat_name, cat_content in course_tree.items():
        stack.append((cat_name, cat_content))

    print(f"--- BẮT ĐẦU DUYỆT CÂY DFS (Gap: {list(gap_dict.keys())}) ---")

    # 2. Vòng lặp DFS
    while stack:
        # Lấy phần tử cuối cùng ra (LIFO - Last In First Out)
        current_node_name, current_node_content = stack.pop()
        
        # 3. Gọi Mock LLM để đánh giá
        is_relevant = mock_llm_evaluate(current_node_name, gap_dict)
        
        if is_relevant:
            print(f"[KEEP] Node '{current_node_name}' có liên quan. Đang khám phá...")
            
            # Kiểm tra xem đây là Node Lá (List) hay Node Nhánh (Dict)
            if isinstance(current_node_content, list):
                # Đã chạm tới danh sách khóa học cụ thể
                candidate_courses.extend(current_node_content)
                print(f"      => Tìm thấy {len(current_node_content)} khóa học tiềm năng.")
            else:
                # Đây là Node Nhánh (ví dụ: Backend -> Java, Python)
                # Đẩy các Node con vào stack để duyệt tiếp
                for sub_name, sub_content in current_node_content.items():
                    stack.append((sub_name, sub_content))
        else:
            print(f"[PRUNE] Cắt tỉa nhánh '{current_node_name}' - Không liên quan.")

    return candidate_courses

# --- TEST CASE TÍCH HỢP GIAI ĐOẠN 1 & 4 ---
if __name__ == "__main__":
    # Bước A: Load dữ liệu và xây cây từ Giai đoạn 1
    flat_data = load_mock_courses("mock_courses.json")
    tree = build_course_tree(flat_data)
    
    # Bước B: Giả lập kết quả Skill Gap từ Giai đoạn 3
    # Người dùng thiếu Java level 2, 3 và Spring Boot level 1, 2
    mock_gap = {
        'Java': [2, 3], 
        'Spring Boot': [1, 2]
    }
    
    # Bước C: Chạy thuật toán tìm kiếm
    found_courses = dfs_tree_search(tree, mock_gap)
    
    # Bước D: In kết quả cuối cùng
    print("\n--- KẾT QUẢ: DANH SÁCH KHÓA HỌC ỨNG VIÊN ---")
    if found_courses:
        for i, c in enumerate(found_courses, 1):
            print(f"{i}. [{c['id']}] {c['title']} (Skill: {', '.join(c['target_skills'])}, Level: {c['level']})")
    else:
        print("Không tìm thấy khóa học nào phù hợp.")