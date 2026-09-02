import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Chẩn Đoán Tư Duy COI - NCKH",
    page_icon="🔬",
    layout="wide",
)

# Custom CSS giao diện
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
    "<div class='main-title'>🔬 HỆ THỐNG BÁO CÁO TRỰC QUAN & CHẨN ĐOÁN CHỈ SỐ"
    " COI</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='sub-title'>Sản phẩm NCKH: Đo lường & Giảm thiểu chỉ số phụ thuộc"
    " AI (COI) ở học sinh THPT</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ==========================================
# 2. KHỐI NHẬP DỮ LIỆU ĐẦU VÀO (SIDEBAR)
# ==========================================
st.sidebar.header("📋 NHẬP THÔNG SỐ HỌC SINH")
student_name = st.sidebar.text_input("Họ và tên học sinh:", "Nguyễn Văn A")
grade = st.sidebar.selectbox("Khối lớp:", ["Khối 10", "Khối 11", "Khối 12"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Chỉ số hành vi thực nghiệm (Dải [0.0, 1.0])")

# Biến 1: C_blind
c_blind = st.sidebar.slider(
    "1. Sao chép mù quáng (C_blind):",
    min_value=0.0,
    max_value=1.0,
    value=0.40,
    step=0.01,
    help=(
        "Tỷ lệ câu chấp nhận/copy hoàn toàn đáp án AI không qua kiểm chứng"
        " phản biện (C_blind ∈ [0, 1])"
    ),
)

# Biến 2: F_off
f_off = st.sidebar.slider(
    "2. Tần suất cầu viện AI (F_off):",
    min_value=0.0,
    max_value=1.0,
    value=0.60,
    step=0.01,
    help="Tỷ lệ câu gửi yêu cầu/prompt cho AI xử lý (F_off ∈ [0, 1])",
)

# Biến 3: T_off
t_off = st.sidebar.slider(
    "3. Độ trễ cầu viện (T_off):",
    min_value=0.0,
    max_value=1.0,
    value=0.17,
    step=0.01,
    help=(
        "Chỉ số nỗ lực tư duy/thời gian suy nghĩ độc lập trước khi cầu viện AI"
        " (T_off ∈ [0, 1])"
    ),
)

# ==========================================
# 3. MÔ HÌNH TOÁN HỌC & TÍNH CHỈ SỐ COI
# Công thức chuẩn: COI = max(0, 30*F_off - 20*T_off + 70*C_blind)
# ==========================================
a, b, c = 30, 20, 70
coi_calc = (a * f_off) - (b * t_off) + (c * c_blind)
coi = round(max(0.0, coi_calc), 2)

# ==========================================
# 4. HIỂN THỊ KẾT QUẢ CHẨN ĐOÁN
# ==========================================
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
  st.subheader(f"👤 Học sinh: **{student_name}** ({grade})")

  m1, m2 = st.columns(2)
  with m1:
    st.metric(label="Chỉ số Phụ thuộc AI (COI)", value=f"{coi} / 100")
  with m2:
    if coi > 60:
      st.error("TRẠNG THÁI: MỨC CAO 🚨")
      st.caption("Nguy cơ lạm dụng & tiêu biến tư duy")
    elif coi >= 30:
      st.warning("TRẠNG THÁI: MỨC TRUNG BÌNH ⚠️")
      st.caption("Có dấu hiệu bắt đầu phụ thuộc")
    else:
      st.success("TRẠNG THÁI: MỨC THẤP ✅")
      st.caption("Giữ vững năng lực tự chủ học tập")

  st.markdown("### 📢 Phân Tích Cơ Chế Tư Duy & Lời Khuyên")
  if coi > 60:
    st.error(
        f"🚨 **CẢNH BÁO LẠM DỤNG:** Tỷ lệ sao chép mù quáng **C_blind ="
        f" {c_blind:.2f}** ({c_blind*100:.0f}%). Theo thuyết *Kẻ bủn xỉn nhận"
        " thức* (Cognitive Miser), bạn đang để AI thay thế hoàn toàn Mạng lưới"
        " Tư duy 2. Hãy dừng thói quen copy-paste và kiểm định bẫy logic của"
        " AI!"
    )
  elif coi >= 30:
    st.warning(
        f"⚠️ **CẢNH BÁO NGUY CƠ:** Độ trễ tư duy **T_off** hiện đạt"
        f" **{t_off:.2f}**. Bạn đang có xu hướng tìm kiếm lối tắt quá nhanh"
        " khi gặp bài tập khó. Hãy áp dụng quy tắc tự nháp ít nhất 10 phút"
        " trước khi mở prompt hỏi AI."
    )
  else:
    st.balloons()
    st.success(
        "🎉 **TƯ DUY ĐỘC LẬP TỐT:** Bạn đang làm chủ công nghệ xuất sắc! AI chỉ"
        " đóng vai trò là 'Công cụ mở rộng nhận thức' (Extended Mind) chứ không"
        " thể thao túng tư duy phản biện của bạn."
    )

  st.markdown("#### 📐 Bảng Giá Trị Biến Số Vào Mô Hình")
  st.json({
      "F_off (Tần suất hỏi AI)": f_off,
      "T_off (Độ trễ cầu viện)": t_off,
      "C_blind (Sao chép mù quáng)": c_blind,
      "Trọng số áp dụng (a, b, c)": [a, b, c],
      "Công thức": "COI = max(0, 30*F_off - 20*T_off + 70*C_blind)",
  })

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

  # Quy đổi về dải 0 - 100 cho đồ thị
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
# 6. THỬ THÁCH TỰ ĐIỀU CHỈNH HÀNH VI (GAMIFICATION)
# ==========================================
st.markdown("---")
st.subheader("🎯 Thử Thách 7 Ngày Tự Điều Chỉnh Hành Vi Học Tập")
st.write(
    "Tích chọn các mục tiêu bạn cam kết thực hiện để nâng cao chỉ số năng lực tự"
    " chủ:"
)

c1, c2 = st.columns(2)
with c1:
  st.checkbox(
      "Thử thách 1: Nâng chỉ số nỗ lực T_off lên tối thiểu 0.50 trước khi cầu"
      " viện AI."
  )
  st.checkbox(
      "Thử thách 2: Sử dụng Socratic Prompting để AI đóng vai gợi mở thay vì cho"
      " đáp án."
  )
with c2:
  st.checkbox(
      "Thử thách 3: Tìm ra ít nhất 1 bẫy ảo giác (Hallucination) trong câu trả"
      " lời của AI."
  )
  st.checkbox(
      "Thử thách 4: Giải hoàn chỉnh 1 bài tập phức tạp mà không sử dụng bất kỳ"
      " công cụ hỗ trợ nào."
  )
