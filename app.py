import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH TRANG WEB & CSS TÙY CHỈNH
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
        margin-bottom: 20px;
    }
    .note-box {
        background-color: #F8FAFC;
        padding: 14px 18px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        font-size: 13px;
        color: #334155;
        margin-top: 10px;
        line-height: 1.6;
    }
    
    /* Thiết kế thẻ Mức độ cảnh báo đẹp mắt */
    .status-card {
        padding: 12px 16px;
        border-radius: 10px;
        text-align: center;
        margin-top: 5px;
    }
    .status-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .status-desc {
        font-size: 13px;
        opacity: 0.9;
    }
    
    /* 3 Mức màu sắc tùy chỉnh */
    .status-danger {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }
    .status-warning {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FCD34D;
    }
    .status-success {
        background-color: #F0FDF4;
        color: #166534;
        border: 1px solid #86EFAC;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Tiêu đề chính
st.markdown(
    "<div class='main-title'>🔬 PHIẾU CHẨN ĐOÁN TƯ DUY CÁ NHÂN (PERSONAL"
    " AI-HEALTH CHECK)</div>",
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
      st.markdown(
          """
            <div class='status-card status-danger'>
                <div class='status-title'>MỨC ĐỘ: CAO 🚨</div>
                <div class='status-desc'>Cảnh báo lạm dụng nghiêm trọng</div>
            </div>
            """,
          unsafe_allow_html=True,
      )
    elif coi >= 30:
      st.markdown(
          """
            <div class='status-card status-warning'>
                <div class='status-title'>MỨC ĐỘ: TRUNG BÌNH ⚠️</div>
                <div class='status-desc'>Có nguy cơ bắt đầu phụ thuộc</div>
            </div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          """
            <div class='status-card status-success'>
                <div class='status-title'>MỨC ĐỘ: THẤP ✅</div>
                <div class='status-desc'>Năng lực tự chủ tư duy tốt</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

  st.markdown("### 📢 Cảnh Báo Thị Giác Trực Quan")

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
        f"⚠️ **CẢNH BÁO THỜI GIAN SUY NGHĨ T_off:** Chỉ số thời gian suy nghĩ"
        f" T_off của bạn hiện ở mức rất thấp (**{t_off:.2f}**). Bạn đang quá"
        " vội vã tìm kiếm 'lối tắt' thay vì tự nháp bài."
    )
  else:
    st.success(f"✅ Chỉ số nỗ lực tư duy T_off đạt mức tích cực: **{t_off:.2f}**.")

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

  # CÔNG THỨC TOÁN HỌC LATEX CHUẨN
  st.markdown("**Công thức toán học tính chỉ số COI:**")
  st.latex(
      r"\text{COI} = \max\left(0,\; 30 \cdot F_{\text{off}} - 20 \cdot"
      r" T_{\text{off}} + 70 \cdot C_{\text{blind}}\right)"
  )

# ==========================================
# 5. VẼ BIỂU ĐỒ RADAR 4 CHIỀU NĂNG LỰC & CHÚ THÍCH
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

  # Thang đo từ 0 đến 100
  ax.set_ylim(0, 100)
  ax.set_yticks([0, 20, 40, 60, 80, 100])
  ax.set_yticklabels(
      ["0", "20", "40", "60", "80", "100"], fontsize=7, color="gray"
  )

  st.pyplot(fig)

  # KHỐI CHÚ THÍCH SẠCH SẼ
  st.markdown(
      """
  <div class='note-box'>
  <b>💡 Hướng dẫn đọc biểu đồ Radar (Thang điểm 0 - 100%):</b><br>
  • <b>Mốc 0 - 100%:</b> Biểu đồ quy đổi toàn bộ chỉ số về phần trăm (%). Mốc <b>0%</b> ở tâm (yếu nhất) và <b>100%</b> ở vòng ngoài cùng (làm chủ hoàn hảo).<br>
  • <b>T_off (Nỗ lực tư duy):</b> Tỷ lệ thời gian nháp/suy nghĩ trước khi bật AI = T_off × 100%.<br>
  • <b>C_blind (Màng lọc phản biện):</b> Khả năng kiểm tra lỗi bài làm = (1 - C_blind) × 100%.<br>
  • <b>F_off (Tính tự lực):</b> Mức độ tự hoàn thành bài tập không cần AI trợ giúp = (1 - F_off) × 100%.<br>
  • <b>Metacognition (Siêu nhận thức):</b> Năng lực tự kiểm soát nhận thức cá nhân = 100 - COI.<br>
  📌 <i><b>Quy tắc thị giác:</b> Diện tích vùng màu phủ càng rộng, năng lực tự chủ tư duy của học sinh càng toàn diện.</i>
  </div>
  """,
      unsafe_allow_html=True,
  )

# ==========================================
# 6. LỘ TRÌNH TỰ ĐIỀU CHỈNH XẾP DỌC (GAMIFICATION)
# ==========================================
st.markdown("---")
st.subheader("🎯 Lộ Trình Gamification: 4 Bước Chuyển Hóa Tư Duy")
st.write(
    "Thực hiện lần lượt các bước dưới đây từ trên xuống dưới để rèn luyện bản"
    " lĩnh tự học:"
)

# Bước 1
st.markdown("##### 🟢 Level 1: Nỗ Lực Tư Duy Độc Lập (T_off)")
st.checkbox(
    "Cam kết tự nháp và suy nghĩ tối thiểu 10–15 phút trước khi mở AI trợ giúp.",
    key="lvl1",
)

st.markdown("---")

# Bước 2
st.markdown(
    "##### 🟡 Level 2: Hỏi Định Hướng & Phương Pháp - Không Hỏi Đáp Án"
)
st.checkbox(
    "Tuyệt đối không xin đáp án trực tiếp. Chỉ yêu cầu AI hướng dẫn phương"
    " hướng, công thức và khung cách làm khi bị bế tắc.",
    key="lvl2",
)

st.markdown("---")

# Bước 3
st.markdown("##### 🟠 Level 3: Kiểm Chứng Phản Biện (C_blind)")
st.checkbox(
    "Đóng vai người kiểm duyệt: Chủ động truy tìm ít nhất 1 lỗi logic hoặc bẫy"
    " ảo giác trong câu trả lời của AI.",
    key="lvl3",
)

st.markdown("---")

# Bước 4
st.markdown("##### 🔴 Level 4: Làm Chủ Công Nghệ Hoàn Toàn")
st.checkbox(
    "Hoàn thành 1 bài tập phức tạp 100% bằng năng lực cá nhân, sau đó chỉ dùng"
    " AI đóng vai trò người phản biện chấm điểm.",
    key="lvl4",
)
