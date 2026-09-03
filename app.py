import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH WEB APP CHUYÊN NGHIỆP
# ==========================================
st.set_page_config(
    page_title="AI Health Check - Chẩn Đoán Tư Duy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ẩn các thành phần thừa của Streamlit & Áp dụng CSS giao diện ứng dụng
st.markdown(
    """
    <style>
    /* Ẩn Header & Footer mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Font hệ thống & Background nền xám nhẹ kiểu App */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Header chính thiết kế dạng Banner hiện đại */
    .app-header {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 32px 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
        text-align: center;
        margin-bottom: 30px;
        color: #FFFFFF;
        position: relative;
    }
    .app-header-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0;
        text-transform: uppercase;
    }
    .app-header-subtitle {
        color: #93C5FD;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 3px;
        margin-top: 6px;
        text-transform: uppercase;
    }
    
    /* Card chứa nội dung dạng App Widget */
    .app-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }

    /* Đổi phong cách các nút bấm (Buttons) */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 3em !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    }

    /* Thẻ trạng thái kết quả */
    .status-card {
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
    }
    .status-danger { background-color: #FEF2F2; color: #991B1B; border: 1px solid #FCA5A5; }
    .status-warning { background-color: #FFFBEB; color: #92400E; border: 1px solid #FCD34D; }
    .status-success { background-color: #F0FDF4; color: #166534; border: 1px solid #86EFAC; }
    
    .eval-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        line-height: 1.6;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Khởi tạo Session State
if "page" not in st.session_state:
  st.session_state.page = 1

# ==========================================
# 2. SIDEBAR NAVIGATION (THANH ĐIỀU HƯỚNG)
# ==========================================
with st.sidebar:
  st.image(
      "https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=60
  )  # Icon ứng dụng
  st.title("AI-Health System")
  st.caption("Phiên bản 2.4 • Enterprise UI")
  st.markdown("---")

  st.subheader("📌 Menu Điều Hướng")
  nav_choice = st.radio(
      "Chọn màn hình:",
      ["1. Nhập liệu & Chỉ số", "2. Báo cáo & Đánh giá"],
      index=0 if st.session_state.page == 1 else 1,
  )

  if nav_choice == "1. Nhập liệu & Chỉ số" and st.session_state.page != 1:
    st.session_state.page = 1
    st.rerun()
  elif nav_choice == "2. Báo cáo & Đánh giá" and st.session_state.page != 2:
    st.session_state.page = 2
    st.rerun()

  st.markdown("---")
  st.info("💡 **Ghi chú:** Điền các chỉ số đo lường ở Màn hình 1 để xuất báo cáo.")

# ==========================================
# MÀN HÌNH 1: NHẬP THÔNG TIN VÀ CHỈ SỐ
# ==========================================
if st.session_state.page == 1:
  st.markdown(
      """
    <div class="app-header">
        <div class="app-header-title">PHIẾU CHẨN ĐOÁN TƯ DUY CÁ NHÂN</div>
        <div class="app-header-subtitle">PERSONAL AI-HEALTH CHECK SYSTEM</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns([1, 1], gap="large")

  with col1:
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("👤 Thông tin học sinh")
    student_name = st.text_input(
        "Họ và tên học sinh:",
        st.session_state.get("student_name", "Nguyễn Văn A"),
        placeholder="Nhập tên học sinh...",
    )
    grade = st.selectbox(
        "Khối lớp:",
        ["Khối 10", "Khối 11", "Khối 12"],
        index=["Khối 10", "Khối 11", "Khối 12"].index(
            st.session_state.get("grade", "Khối 10")
        ),
    )
    st.markdown("</div>", unsafe_allow_html=True)

  with col2:
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Chỉ số hành vi thực nghiệm")

    c_blind = st.slider(
        "1. Tỷ lệ sao chép mù quáng (C_blind):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("c_blind", 0.4), 1),
        step=0.1,
        help="Tỷ lệ bài làm chép nguyên văn từ AI không qua kiểm chứng",
    )

    f_off = st.slider(
        "2. Tần suất cầu viện AI (F_off):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("f_off", 0.6), 1),
        step=0.1,
        help="Tỷ lệ câu hỏi gửi lệnh cho AI xử lý",
    )

    t_off = st.slider(
        "3. Thời gian suy nghĩ độc lập (T_off):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("t_off", 0.17), 2),
        step=0.01,
        help="Chỉ số nỗ lực tư duy trước khi nhờ sự hỗ trợ từ AI",
    )
    st.markdown("</div>", unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🚀 XUẤT BÁO CÁO PHÂN TÍCH CHUYÊN SÂU", use_container_width=True):
    st.session_state.student_name = student_name
    st.session_state.grade = grade
    st.session_state.c_blind = c_blind
    st.session_state.f_off = f_off
    st.session_state.t_off = t_off
    st.session_state.page = 2
    st.rerun()

# ==========================================
# MÀN HÌNH 2: BÁO CÁO KẾT QUẢ & ĐÁNH GIÁ
# ==========================================
elif st.session_state.page == 2:
  student_name = st.session_state.get("student_name", "N/A")
  grade = st.session_state.get("grade", "N/A")
  c_blind = st.session_state.get("c_blind", 0.0)
  f_off = st.session_state.get("f_off", 0.0)
  t_off = st.session_state.get("t_off", 0.0)

  a, b, c = 30, 20, 70
  coi_calc = (a * f_off) - (b * t_off) + (c * c_blind)
  coi = round(max(0.0, coi_calc), 2)

  st.markdown(
      """
    <div class="app-header">
        <div class="app-header-title">BÁO CÁO CHẨN ĐOÁN TỰ NHẬN THỨC COI</div>
        <div class="app-header-subtitle">AI DEPENDENCE INDEX REPORT</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  col_left, col_right = st.columns([1.1, 0.9], gap="large")

  with col_left:
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.markdown(f"### 👤 Hồ sơ: **{student_name}** • `{grade}`")

    m1, m2 = st.columns(2)
    with m1:
      st.metric(label="Chỉ số Phụ thuộc AI (COI)", value=f"{coi} / 100")
    with m2:
      if coi > 60:
        st.markdown(
            """
                <div class='status-card status-danger'>
                    <div>MỨC ĐỘ: CAO 🚨</div>
                    <small>Cảnh báo lạm dụng nghiêm trọng</small>
                </div>
                """,
            unsafe_allow_html=True,
        )
      elif coi >= 30:
        st.markdown(
            """
                <div class='status-card status-warning'>
                    <div>MỨC ĐỘ: TRUNG BÌNH ⚠️</div>
                    <small>Có nguy cơ phụ thuộc</small>
                </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.markdown(
            """
                <div class='status-card status-success'>
                    <div>MỨC ĐỘ: THẤP ✅</div>
                    <small>Tự chủ tư duy rất tốt</small>
                </div>
                """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📢 Cảnh Báo Thị Giác")
    if c_blind >= 0.5:
      st.error(
          f"🚨 **CẢNH BÁO SỬ DỤNG AI MÙ QUÁNG:** Đã dành"
          f" **{c_blind*100:.0f}%** bài làm để chép từ AI mà không qua kiểm"
          " chứng!"
      )
    else:
      st.info(
          f"💡 Tỷ lệ chấp nhận đáp án AI chưa qua kiểm định:"
          f" **{c_blind*100:.0f}%**."
      )

    if t_off <= 0.3:
      st.warning(
          f"⚠️ **CẢNH BÁO THỜI GIAN SUY NGHĨ T_off:** Chỉ số suy nghĩ độc lập"
          f" ở mức thấp (**{t_off:.2f}**)."
      )
    else:
      st.success(f"✅ Chỉ số nỗ lực tư duy T_off tích cực: **{t_off:.2f}**.")

    st.markdown("#### 📐 Bảng Số Liệu Chi Tiết")
    data = {
        "Chỉ số hành vi": [
            "1. Tỷ lệ dán mù (C_blind)",
            "2. Tần suất hỏi AI (F_off)",
            "3. Thời gian suy nghĩ (T_off)",
        ],
        "Giá trị": [
            f"{c_blind*100:.0f}% ({c_blind})",
            f"{f_off*100:.0f}% ({f_off})",
            f"{t_off:.2f}",
        ],
        "Trọng số": [f"c = {c}", f"a = {a}", f"b = {b}"],
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

  with col_right:
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Biểu Đồ Radar Năng Lực")

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

    fig, ax = plt.subplots(figsize=(4.5, 4.5), subplot_kw=dict(polar=True))
    color_code = (
        "#EF4444" if coi > 60 else ("#F59E0B" if coi >= 30 else "#10B981")
    )

    ax.plot(angles, stats, color=color_code, linewidth=2, linestyle="solid")
    ax.fill(angles, stats, color=color_code, alpha=0.25)
    ax.set_thetagrids(
        np.degrees(angles[:-1]), labels, fontsize=9, fontweight="bold"
    )

    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(
        ["0", "20", "40", "60", "80", "100"], fontsize=7, color="gray"
    )

    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

  # Đánh giá & Lộ trình Gamification
  st.markdown("<div class='app-card'>", unsafe_allow_html=True)
  st.markdown("### 📝 ĐÁNH GIÁ TỰ NHẬN THỨC CHI TIẾT")

  if coi < 30:
    st.markdown(
        f"""
        <div class='eval-box status-success'>
        <h4>🟢 MỨC ĐỘ THẤP (COI = {coi:.2f}): TỰ CHỦ VÀ TƯ DUY TỐT</h4>
        Học sinh làm chủ hoàn toàn quá trình học tập. AI chỉ đóng vai trò hỗ trợ mở rộng kiến thức.
        </div>
        """,
        unsafe_allow_html=True,
    )
  elif coi <= 60:
    st.markdown(
        f"""
        <div class='eval-box status-warning'>
        <h4>🟡 MỨC ĐỘ TRUNG BÌNH (COI = {coi:.2f}): NGUY CƠ PHỤ THUỘC AI</h4>
        Học sinh có dấu hiệu phụ thuộc thói quen khi gặp bài khó hoặc áp lực thời gian.
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"""
        <div class='eval-box status-danger'>
        <h4>🔴 MỨC ĐỘ CAO (COI = {coi:.2f}): CẢNH BÁO LẠM DỤNG</h4>
        Cảnh báo: Lạm dụng AI mức độ cao có thể gây tiêu biến năng lực tự duy độc lập.
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.markdown("### 🎯 LỘ TRÌNH RÈN LUYỆN (GAMIFICATION)")
  c1, c2 = st.columns(2)
  with c1:
    st.checkbox("🟢 Level 1: Nháp tối thiểu 15 phút trước khi hỏi AI.", key="l1")
    st.checkbox(
        "🟡 Level 2: Chỉ xin gợi ý phương pháp, không xin đáp án.", key="l2"
    )
  with c2:
    st.checkbox("🟠 Level 3: Chủ động tìm 1 lỗi sai/logic từ AI.", key="l3")
    st.checkbox(
        "🔴 Level 4: Tự làm 100% bài phức tạp rồi nhờ AI phản biện.", key="l4"
    )

  st.markdown("</div>", unsafe_allow_html=True)
