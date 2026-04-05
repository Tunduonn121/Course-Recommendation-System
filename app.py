from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

# Import 4 Module cốt lõi của hệ thống
from data_loader import load_mock_courses, build_course_tree
from skill_extractor import extract_skills_from_jd
from skill_gap_calculator import compute_skill_gap
from tree_searcher import dfs_tree_search
from course_ranker import rank_courses_with_llm

app = Flask(__name__)

# 1. Nạp môi trường và API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Chuẩn bị Dữ liệu (Load 1 lần duy nhất khi khởi động Server)
flat_data = load_mock_courses("mock_courses.json")
course_tree = build_course_tree(flat_data)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Lấy văn bản từ giao diện Web
        cv_text = request.form.get("cv_text")
        jd_text = request.form.get("jd_text")

        # GIAI ĐOẠN 2: AI Trích xuất Kỹ năng
        # (Sử dụng chung hàm extract cho cả CV và JD vì logic rút trích từ khóa IT là giống nhau)
        cv_skills = extract_skills_from_jd(cv_text, API_KEY)
        jd_skills = extract_skills_from_jd(jd_text, API_KEY)

        # GIAI ĐOẠN 3: Tính toán Khoảng trống học bù (Progressive Skill Gap)
        gap_dict = compute_skill_gap(cv_skills, jd_skills)

        # Nếu không có gap, trả về thông báo rỗng
        if not gap_dict:
            return render_template("index.html", 
                                   cv_skills=cv_skills, 
                                   jd_skills=jd_skills, 
                                   gap_dict="Bạn đã đáp ứng đủ yêu cầu, không có khoảng trống!", 
                                   ranked_courses=[])

        # GIAI ĐOẠN 4.1: Duyệt cây DFS để tìm danh sách ứng viên
        candidate_courses = dfs_tree_search(course_tree, gap_dict)

        # GIAI ĐOẠN 4.2: Gọi AI xếp hạng theo Luật Sư Phạm
        ranked_courses = rank_courses_with_llm(candidate_courses, gap_dict, API_KEY, top_k=3)

        # Trả toàn bộ dữ liệu về cho HTML hiển thị
        return render_template("index.html", 
                               cv_skills=cv_skills, 
                               jd_skills=jd_skills, 
                               gap_dict=gap_dict, 
                               ranked_courses=ranked_courses)

    # Nếu là giao diện load lần đầu (GET)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)