import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Báo Cáo Tự Nhận Thức COI - NCKH",
    page_icon="🔬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 14px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='main-title'>🔬 PHIẾU CHẨN ĐOÁN TƯ DUY CÁ NHÂN (PERSONAL"
    " AI-HEALTH CHECK)</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='sub-title'>Giải pháp 3: Phát triển ứng dụng Báo cáo tự nhận"
    " thức COI dành riêng cho Học sinh</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ==========================================
# 2. KHỐI NHẬP DỮ LIỆU ĐẦU VÀO (SIDEBAR)
# ==========================================
st.sidebar.header("📋 THÔNG TIN HỌC SINH")
student_name = st.sidebar.text_input("Họ và tên học sinh:", "Nguyễn Văn A")
grade = st.sidebar.selectbox("Khối lớp:", ["Khối 10", "Khối 11", "Khối 12"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Chỉ Số Hành Vi Thực Nghiệm")

# Biến 1: C_blind
c_blind = st.sidebar.slider(
    "1. Sao chép mù quáng (C_blind):",
    min_value=0.0,
    max_value=1.0,
    value=0.40,
    step=0.01,
    help="Tỷ lệ bài làm chép nguyên văn từ AI không qua kiểm chứng (C_blind ∈ [0, 1])",
)

# Biến 2: F_off
f_off = st.sidebar.slider(
    "2. Tần suất cầu viện AI (F_off):",
    min_value=0.0,
    max_value=1.0,
    value=0.60,
    step=0.01,
    help="Tỷ lệ câu hỏi gửi lệnh cho AI xử lý (F_off ∈ [0, 1])",
)

# Biến 3: T_off
t_off = st.sidebar.slider(
    "3. Thời gian suy nghĩ độc lập (T_off):",
    min_value=0.0,
    max_value=1.0,
    value=0.17,
    step=0.01,
    help="Chỉ số thời gian/nỗ lực suy nghĩ trước khi hỏi AI (T_off ∈ [0, 1])",
)

# ==========================================
# 3. MÔ HÌNH TOÁN HỌC & TÍNH CHỈ SỐ COI
# Công thức chuẩn: COI = max(0, 30*F_off - 20*T_off + 70*C_blind)
# ==========================================
a, b, c = 30, 20, 70
coi_calc = (a * f_off) - (b * t_off) + (c * c_blind)
coi = round(max(0.0, coi_calc), 2)

# ==========================================
# 4. HIỂN THỊ KẾT QUẢ CHẨN ĐOÁN & CẢNH BÁO THỊ GIÁC
# ==========================================
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
  st.subheader(f"👤 Học sinh: **{student_name}** ({grade})")

  m1, m2 = st.columns(2)
  with m1:
    st.metric(label="Chỉ số Phụ thuộc AI (COI)", value=f"{coi} / 100")
  with m2:
    if coi > 60:
      st.error("MỨC ĐỘ: CAO 🚨")
      st.caption("Cảnh báo lạm dụng nghiêm trọng")
    elif coi >= 30:
      st.warning("MỨC ĐỘ: TRUNG BÌNH ⚠️")
      st.caption("Có nguy cơ bắt đầu phụ thuộc")
    else:
      st.success("MỨC ĐỘ: THẤP ✅")
      st.caption("Năng lực tự chủ tư duy tốt")

  st.markdown("### 📢 Cảnh Báo Thị Giác Trực Quan")
  
  # Cảnh báo thị giác chuẩn hóa theo đúng ví dụ trong tài liệu
  if c_blind >= 0.5:
    st.error(
        f"🚨 **CẢNH BÁO SỬ DỤNG AI MÙ QUÁNG:** Bạn đã dành"
        f" **{c_blind*100:.0f}%** bài làm để chép từ AI mà không qua kiểm"
        " chứng phản biện! Hãy dừng ngay việc copy-paste để tránh tiêu biến"
        " tư duy độc lập."
    )
  else:
    st.info(f"💡 Tỷ lệ chấp nhận đáp án AI chưa qua kiểm định: **{c_blind*100:.0f}%**.")

  if t_off <= 0.3:
    st.warning(
        f"⚠️ **CẢNH BÁO THỜI GIAN SUY NGHĨ $T_{{off}}$:** Chỉ số thời gian suy"
        f" nghĩ $T_{{off}}$ của bạn hiện ở mức rất thấp (**{t_off:.2f}**). Bạn"
        " đang quá vội vã tìm kiếm 'lối tắt' thay vì tự nháp bài."
    )
  else:
    st.success(f"✅ Chỉ số nỗ lực tư duy $T_{{off}}$ đạt mức tích cực: **{t_off:.2f}**.")

  # Bảng giá trị thông số thực nghiệm
  st.markdown("#### 📐 Bảng Thông Số Chẩn Đoán Dữ Liệu")
  data = {
      "Chỉ số hành vi": [
          "1. Tỷ lệ dán mù (C_blind)",
          "2. Tần suất hỏi AI (F_off)",
          "3. Thời gian suy nghĩ (T_off)",
      ],
      "Giá trị đo lường": [
          f"{c_blind*100:.0f}% ({c_blind})",
          f"{f_off*100:.0f}% ({f_off})",
          f"{t_off:.2f}",
      ],
      "Trọng số mô hình": [f"c = {c}", f"a = {a}", f"b = {b}"],
  }
  df = pd.DataFrame(data)
  st.dataframe(df, use_container_width=True, hide_index=True)
  st.info("**Công thức COI:** `COI = max(0, 30*F_off - 20*T_off + 70*C_blind)`")

# ==========================================
# 5. VẼ BIỂU ĐỒ RADAR 4 CHIỀU NĂNG LỰC
# ==========================================
with col_right:
  st.subheader("📊 Biểu Đồ Radar Năng Lực Tự Chủ")

  labels = np.array([
      "T_off\n(Nỗ lực tư duy)",
      "C_blind\n(Màng lọc phản biện)",
      "F_off\n(Tính tự lực)",
      "Metacognition\n(Siêu nhận thức)",
  ])

  stats = [
      t_off * 100,
      (1 - c_blind) * 100,
      (1 - f_off) * 100,
      max(0, 100 - coi),
  ]

  angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
  stats = np.concatenate((stats, [stats[0]]))
  angles = np.concatenate((angles, [angles[0]]))

  fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
  color_code = "#FF4B4B" if coi > 60 else ("#FFAA00" if coi >= 30 else "#00CC66")

  ax.plot(angles, stats, color=color_code, linewidth=2, linestyle="solid")
  ax.fill(angles, stats, color=color_code, alpha=0.25)
  ax.set_thetagrids(
      np.degrees(angles[:-1]), labels, fontsize=9, fontweight="bold"
  )
  ax.set_ylim(0, 100)

  st.pyplot(fig)

# ==========================================
# 6. LỘ TRÌNH TỰ ĐIỀU CHỈNH (GAMIFICATION)
# ==========================================
st.markdown("---")
st.subheader("🎯 Lộ Trình Tự Điều Chỉnh (Gamification)")
st.write(
    "Hãy tích chọn các thử thách cá nhân hóa dưới đây để rèn luyện bản lĩnh tự"
    " học và nâng cao năng lực tự chủ:"
)

c1, c2 = st.columns(2)
with c1:
  st.checkbox(
      "Thử thách 1: Nâng chỉ số thời gian suy nghĩ T_off lên mức tối thiểu 0.50"
      " trước khi tìm trợ giúp từ AI."
  )
  st.checkbox(
      "Thử thách 2: Thử thách tự phát hiện ít nhất 3 bẫy ảo giác (Hallucination)"
      " hoặc lỗi sai của AI trong bài học."
  )
with c2:
  st.checkbox(
      "Thử thách 3: Sử dụng Socratic Prompting (yêu cầu AI đặt câu hỏi gợi mở"
      " thay vì đưa lời giải trực tiếp)."
  )
  st.checkbox(
      "Thử thách 4: Hoàn thành 1 bài tập phức tạp 100% bằng tư duy cá nhân mà"
      " không sử dụng công cụ AI."
  )
