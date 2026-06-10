# (1) Phân tích & Clean Code
# 1. Đặt tên biến và hàm theo chuẩn PEP 8
# match_list
# match_id
# team_a
# team_b
# display_matches()
# update_score()
# generate_report()
# determine_winner()

# 2. Viết Docstrings cho các hàm
# Mỗi hàm cần có docstring để mô tả chức năng, tham số đầu vào và giá trị trả về

# 3. Cấu hình Logging
# Sử dụng thư viện logging để ghi lại các thao tác và lỗi phát sinh trong hệ thống
# File log:
# tournament_app.log
# Định dạng:
# [Thời gian] - [Cấp độ Log] - [Tin nhắn]

# (2) Triển khai Code (Refactoring & Exception)
import logging

logging.basicConfig(
    filename="tournament_app.log",
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s"
)
matches = [
    {"match_id": "M01", "team_a": "T1", "team_b": "GenG",
     "score_a": 2, "score_b": 1, "status": "Completed"},
    {"match_id": "M02", "team_a": "JDG", "team_b": "BLG",
     "score_a": 0, "score_b": 0, "status": "Pending"}
]

def display_matches(match_list):
    """Hiển thị danh sách trận đấu."""
    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return
    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    for match in match_list:
        try:
            print(
                f"{match['match_id']} | "
                f"{match['team_a']} vs {match['team_b']} | "
                f"{match['score_a']}-{match['score_b']} | "
                f"{match['status']}"
            )
        except KeyError:
            logging.error("Thiếu dữ liệu trận đấu")
    logging.info("User viewed the match list.")

def add_match(match_list):
    """Thêm trận đấu mới."""
    match_id = input("Nhập mã trận: ").strip()
    if not match_id:
        logging.warning("Empty match ID")
        return
    for match in match_list:
        if match["match_id"] == match_id:
            logging.warning(f"Match ID {match_id} already exists")
            return
    team_a = input("Đội A: ").strip()
    team_b = input("Đội B: ").strip()
    if not team_a or not team_b:
        logging.warning("Empty team name")
        return
    match_list.append({
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    })
    logging.info(f"Match {match_id} added successfully")

def input_score(message):
    """Nhập điểm hợp lệ."""
    while True:
        try:
            score = int(input(message))
            if score < 0:
                print("Điểm phải >= 0")
                logging.error("Negative score")
                continue
            return score
        except ValueError as error:
            print("Điểm phải là số nguyên")
            logging.error(error)

def update_score(match_list):
    """Cập nhật tỷ số."""
    match_id = input("Nhập mã trận: ").strip()
    for match in match_list:
        if match["match_id"] == match_id:
            score_a = input_score("Điểm đội A: ")
            score_b = input_score("Điểm đội B: ")
            match["score_a"] = score_a
            match["score_b"] = score_b
            if score_a == 0 and score_b == 0:
                confirm = input(
                    "Xác nhận hoàn thành? (y/n): "
                ).lower()
                match["status"] = (
                    "Completed" if confirm == "y"
                    else "Pending"
                )
            else:
                match["status"] = "Completed"

            logging.info(
                f"Match {match_id} score updated successfully"
            )
            return
    logging.warning(
        f"User tried to update non-existing match {match_id}"
    )

def determine_winner(match):
    """Xác định đội thắng."""
    if match["status"] == "Pending":
        return "Not Started"
    if match["score_a"] > match["score_b"]:
        return match["team_a"]
    if match["score_b"] > match["score_a"]:
        return match["team_b"]
    return "Draw"

def generate_report(match_list):
    """Tạo báo cáo."""
    completed = 0
    for match in match_list:
        if match["status"] == "Completed":
            print(
                f"{match['match_id']} - "
                f"{determine_winner(match)}"
            )
            completed += 1
    print(f"Tổng số trận hoàn thành: {completed}")
    logging.info("User generated tournament report.")

def main():
    while True:
        print("\n1. Hiển thị")
        print("2. Thêm trận")
        print("3. Cập nhật tỷ số")
        print("4. Báo cáo")
        print("5. Thoát")
        choice = input("Chọn: ")
        if choice == "1":
            display_matches(matches)
        elif choice == "2":
            add_match(matches)
        elif choice == "3":
            update_score(matches)
        elif choice == "4":
            generate_report(matches)
        elif choice == "5":
            logging.info("Tournament system closed.")
            break
        else:
            print("Lựa chọn không hợp lệ.")
            logging.warning("Invalid menu choice selected")

if __name__ == "__main__":
    main()