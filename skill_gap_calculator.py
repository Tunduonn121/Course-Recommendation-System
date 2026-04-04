def compute_skill_gap(su_dict, sj_dict):
    """
    Tính toán khoảng trống kỹ năng (Skill Gap) dựa trên phương pháp học bù tịnh tiến.
    
    Args:
        su_dict (dict): Dữ liệu kỹ năng từ CV (ví dụ: {"Java": 1})
        sj_dict (dict): Dữ liệu kỹ năng từ JD (ví dụ: {"Java": 3, "Spring Boot": 2})
        
    Returns:
        dict: Dictionary chứa danh sách các cấp độ cần học bù cho mỗi kỹ năng bị thiếu.
    """
    gap_dict = {} # Khởi tạo Dictionary rỗng để chứa kết quả
    
    # Lặp qua từng kỹ năng và cấp độ yêu cầu trong JD
    for skill, job_level in sj_dict.items():
        
        # Kiểm tra xem skill đó có trong CV không. 
        # Hàm .get(key, default) rất tiện: nếu không có key, nó sẽ trả về số 0.
        user_level = su_dict.get(skill, 0)
        
        # So sánh cấp độ
        if user_level < job_level:
            # Tạo mảng tịnh tiến (progressive levels)
            # Lưu ý: Hàm range(start, stop) của Python không bao gồm giá trị stop, 
            # nên ta phải cộng 1 vào job_level (job_level + 1) để lấy được giá trị cuối cùng.
            progressive_levels = list(range(user_level + 1, job_level + 1))
            
            # Lưu mảng này vào gap_dict
            gap_dict[skill] = progressive_levels
            
    return gap_dict

# --- TEST CASE ---
if __name__ == "__main__":
    # 1. Dữ liệu đầu vào
    cv_skills = {"Java": 1}
    jd_skills = {"Java": 3, "Spring Boot": 2,"SQLSever":3}
    
    # 2. Chạy hàm
    result = compute_skill_gap(cv_skills, jd_skills)
    
    # 3. In kết quả
    print("--- CHẠY TEST CASE: PROGRESSIVE SKILL GAP ---")
    print(f"Input CV ($S_u$): {cv_skills}")
    print(f"Input JD ($S_j$): {jd_skills}")
    print(f"Output Gap: {result}")
    
    # 4. Kiểm tra chéo với Expected Output
    expected_output = {"Java": [2, 3], "Spring Boot": [1, 2]}
    if result == expected_output:
        print("\n✅ TEST PASSED: Logic thuật toán chạy chuẩn xác 100%!")
    else:
        print("\n❌ TEST FAILED: Hãy kiểm tra lại code.")