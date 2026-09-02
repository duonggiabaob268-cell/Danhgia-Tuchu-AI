import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Phiếu Chẩn Đoán Tự Nhận Thức COI - NCKH",
    page_icon="🔬",
    layout="centered",
)

st.title("🔬 BÁO CÁO CHẨN ĐOÁN HÀNH VI SỬ DỤNG AI")
st.caption(
    "Sản phẩm thuộc Đề tài NCKH: Đo lường & Giảm thiểu chỉ số phụ thuộc AI"
    " (COI) ở học sinh THPT"
)
st.markdown("---")

# ==========================================
# 2. KHỐI NHẬP DỮ LIỆU ĐẦU VÀO (SIDEBAR)
# ==========================================
st.sidebar.header("📋 NHẬP THÔNG SỐ HỌC SINH")
student_name = st.sidebar.text_input("Họ và tên học sinh:", "Nguyễn Văn A")
grade = st.sidebar.selectbox("Khối lớp:", ["Khối 10", "Khối 11", "Khối 12"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Các chỉ số hành vi thực nghiệm (Bài test 10 câu)")

# Biến C_blind: Số câu dán mù (0 -> 10 câu)
c_blind_raw = st.sidebar.slider(
    "1. Số câu dán mù (C_blind):",
    min_value=0,
    max_value=10,
    value=4,
    help="Số câu copy nguyên văn đáp án AI không qua kiểm duyệt (trên tổng 10 câu)",
)

# Biến F_off: Số câu có hỏi AI (0 -> 10 câu)
f_off_raw = st.sidebar.slider(
    "2. Số câu hỏi AI (F_off):",
    min_value=0,
    max_value=10,
    value=6,
    help="Số câu học sinh gửi lệnh hỏi/prompt cho AI (trên tổng 10 câu)",
)

# Biến T_off: Thời gian suy nghĩ trung bình trước khi hỏi AI (0 -> 150 giây)
t_off_raw = st.sidebar.slider(
    "3. Thời gian suy nghĩ trung bình trước khi hỏi AI (T_off_tb - giây):",
    min_value=0,
    max_value=150,
    value=15,
    help="Thời gian trung bình học sinh đọc đề/nháp trước khi bấm nút hỏi AI",
)

# ==========================================
# 3. CHUẨN HÓA CÁC BIẾN SỐ VỀ ĐOẠN [0, 1] (THEO LÝ THUYẾT)
# ==========================================
# Trọng số chuẩn hóa theo cơ sở lý thuyết NCKH
a = 30  # Trọng số F_off (Tần suất hỏi AI)
b = 20  # Trọng số T_off (Độ trễ cầu viện / Nỗ lực tư duy)
c = 70  # Trọng số C_blind (Sao chép mù quáng)

# Chuẩn hóa biến F_off và C_blind về dải [0, 1] theo tỷ lệ/10 câu
F_off = f_off_raw / 10.0
C_blind = c_blind_raw / 10.0

# Chuẩn hóa T_off theo công thức điểm neo động: T_off = min(1, T_off_tb / 90)
T_off = min(1.0, t_off_raw / 90.0)

# ==========================================
# 4. THUẬT TOÁN TÍNH CHỈ SỐ COI THEO FILE LÝ THUYẾT
# Công thức: COI = max(0, a*F_off - b*T_off + c*C_blind)
# ==========================================
coi_calc = (a * F_off) - (b * T_off) + (c * C_blind)
coi = round(max(0.0, coi_calc), 2)

# ==========================================
# 5. HIỂN THỊ KẾT QUẢ & CẢNH BÁO THỊ GIÁC
# ==========================================
st.subheader(f"👤 Học sinh: **{student_name}** — *{grade}*")

col1, col2 = st.columns([1, 1])

with col1:
  st.metric(label="CHỈ SỐ PHỤ THUỘC AI (COI)", value=f"{coi} / 100")

with col2:
  if coi > 60:
    st.error("TRẠNG THÁI: MỨC CAO 🚨")
    st.caption("Cảnh báo: Lạm dụng nghiêm trọng")
  elif coi >= 30:
    st.warning("TRẠNG THÁI: MỨC TRUNG BÌNH ⚠️")
    st.caption("Cảnh báo: Có nguy cơ phụ thuộc")
  else:
    st.success("TRẠNG THÁI: MỨC THẤP ✅")
    st.caption("Đánh giá: Năng lực tự chủ tốt")

# Phân tích chi tiết theo lý thuyết
st.markdown("### 📢 Phân tích & Lời khuyên tự nhận thức")
if coi > 60:
  st.error(
      f"🚨 **CẢNH BÁO NGUY CƠ:** Bạn có tỷ lệ dán mù **C_blind ="
      f" {C_blind*100:.0f}%** ({c_blind_raw}/10 câu). Theo thuyết *Kẻ bủn xỉn"
      " nhận thức*, bạn đang để AI thay thế hoàn toàn Hệ thống tư duy 2."
      " Hãy dừng việc copy-paste và kiểm định bẫy logic!"
  )
elif coi >= 30:
  st.warning(
      f"⚠️ **LƯU Ý ĐIỀU CHỈNH:** Độ trễ tư duy **T_off** của bạn đạt"
      f" **{T_off:.2f}** ({t_off_raw} giây/câu so với định mức 90s). Bạn"
      " bắt đầu tìm kiếm 'lối tắt' quá nhanh. Hãy áp dụng Quy tắc 10 phút tự"
      " nháp trước khi hỏi AI."
  )
else:
  st.balloons()
  st.success(
      "🎉 **TUYỆT VỜI:** Bạn giữ được tư duy độc lập rất tốt! Bạn chỉ xem AI"
      " như công cụ mở rộng nhận thức (Extended Mind) chứ không bị phụ thuộc"
      " thụ động."
  )

st.markdown("---")

# ==========================================
# 6. VẼ BIỂU ĐỒ RADAR 4 CHIỀU NĂNG LỰC
# ==========================================
st.subheader("📊 Biểu đồ Radar 4 chiều năng lực tự chủ học tập")

labels = np.array([
    "T_off\n(Nỗ lực tư duy)",
    "C_blind\n(Màng lọc phản biện)",
    "F_off\n(Tính tự lực)",
    "Metacognition\n(Siêu nhận thức)",
])

# Quy đổi các thông số về thang điểm năng lực 0 - 100
stats = [
    T_off * 100,  # T_off chuẩn hóa (càng gần 1 càng tốt)
    (1 - C_blind) * 100,  # Kháng dán mù (C_blind càng thấp càng tốt)
    (1 - F_off) * 100,  # Tính tự lực (F_off càng thấp càng tốt)
    max(0, 100 - coi),  # Điểm Siêu nhận thức tổng quát
]

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
stats = np.concatenate((stats, [stats[0]]))
angles = np.concatenate((angles, [angles[0]]))

fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
color_code = "#FF4B4B" if coi > 60 else ("#FFAA00" if coi >= 30 else "#00CC66")

ax.plot(angles, stats, color=color_code, linewidth=2, linestyle="solid")
ax.fill(angles, stats, color=color_code, alpha=0.3)
ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=10, fontweight="bold")
ax.set_ylim(0, 100)

st.pyplot(fig)

# ==========================================
# 7. THỬ THÁCH TỰ ĐIỀU CHỈNH (GAMIFICATION)
# ==========================================
st.markdown("---")
st.subheader("🎯 Lộ trình thử thách 7 ngày nâng cao năng lực tự chủ")
st.write("Hãy tích chọn các thử thách bạn cam kết hoàn thành trong tuần này:")

st.checkbox(
    "Thử thách 1: Nâng thời gian suy nghĩ T_off_tb lên trên 90 giây trước khi"
    " tìm gợi ý."
)
st.checkbox(
    "Thử thách 2: Sử dụng Prompt Socratic để yêu cầu AI đặt câu hỏi gợi mở"
    " thay vì cho lời giải."
)
st.checkbox(
    "Thử thách 3: Đóng vai 'Giám khảo' phát hiện 3 bẫy ảo giác (Hallucination)"
    " của AI."
)
st.checkbox(
    "Thử thách 4: Tự giải hoàn chỉnh 1 bài tập phức tạp mà không sử dụng bất"
    " kỳ công cụ AI nào."
)
