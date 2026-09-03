import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH TRANG WEB & CSS TÙY CHỈNH
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Chẩn Đoán Tư Duy COI",
    page_icon="🔬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-header-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
        padding: 24px 30px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-title-text {
        background: linear-gradient(90deg, #FFFFFF 0%, #E0F2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    .sub-title-text {
        color: #93C5FD;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 2px;
        margin-top: 6px;
        text-transform: uppercase;
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
    .status-card {
        padding: 14px 18px;
        border-radius: 10px;
        text-align: center;
    }
    .status-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .status-desc {
        font-size: 13px;
        opacity: 0.9;
    }
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
    .eval-box {
        padding: 16px;
        border-radius: 10px;
        margin-top: 10px;
        line-height: 1.6;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Khởi tạo trạng thái chuyển trang
if "page" not in st.session_state:
  st.session_state.page = 1

# ==========================================
# TRANG 1: NHẬP THÔNG TIN VÀ CHỈ SỐ
# ==========================================
if st.session_state.page == 1:
  st.markdown(
      """
    <div class="main-header-container">
        <div class="main-title-text">
            <span>🔬</span> PHIẾU CHẨN ĐOÁN TƯ DUY CÁ NHÂN
        </div>
        <div class="sub-title-text">PERSONAL AI-HEALTH CHECK</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  col_center1, col_center2, col_center3 = st.columns([1, 2, 1])

  with col_center2:
    st.markdown("### 📋 Nhập thông tin học sinh")
    student_name = st.text_input(
        "Họ và tên học sinh:",
        st.session_state.get("student_name", "Nguyễn Văn A"),
    )
    grade = st.selectbox(
        "Khối lớp:",
        ["Khối 10", "Khối 11", "Khối 12"],
        index=["Khối 10", "Khối 11", "Khối 12"].index(
            st.session_state.get("grade", "Khối 10")
        ),
    )

    st.markdown("---")
    st.markdown("### ⚙️ Nhập các chỉ số hành vi thực nghiệm")

    c_blind = st.slider(
        "1. Tỷ lệ sao chép mù quáng (C_blind):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("c_blind", 0.4), 1),
        step=0.1,
        format="%.1f",
        help=(
            "Tỷ lệ bài làm chép nguyên văn từ AI không qua kiểm chứng (C_blind ∈"
            " [0, 1])"
        ),
    )

    f_off = st.slider(
        "2. Tần suất cầu viện AI (F_off):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("f_off", 0.6), 1),
        step=0.1,
        format="%.1f",
        help="Tỷ lệ câu hỏi gửi lệnh cho AI xử lý (F_off ∈ [0, 1])",
    )

    t_off = st.slider(
        "3. Thời gian suy nghĩ độc lập (T_off):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("t_off", 0.17), 2),
        step=0.01,
        format="%.2f",
        help=(
            "Chỉ số thời gian/nỗ lực suy nghĩ trước khi hỏi AI (T_off ∈ [0, 1])"
        ),
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(
        "🚀 XUẤT BÁO CÁO KẾT QUẢ & ĐÁNH GIÁ", use_container_width=True
    ):
      st.session_state.student_name = student_name
      st.session_state.grade = grade
      st.session_state.c_blind = c_blind
      st.session_state.f_off = f_off
      st.session_state.t_off = t_off

      st.session_state.page = 2
      st.rerun()

# ==========================================
# TRANG 2: BÁO CÁO KẾT QUẢ & LỘ TRÌNH
# ==========================================
elif st.session_state.page == 2:
  student_name = st.session_state.student_name
  grade = st.session_state.grade
  c_blind = st.session_state.c_blind
  f_off = st.session_state.f_off
  t_off = st.session_state.t_off

  a, b, c = 30, 20, 70
  coi_calc = (a * f_off) - (b * t_off) + (c * c_blind)
  coi = round(max(0.0, coi_calc), 2)

  if st.button("⬅️ Nhập lại thông tin"):
    st.session_state.page = 1
    st.rerun()

  st.markdown(
      """
    <div class="main-header-container">
        <div class="main-title-text">
            <span>📊</span> BÁO CÁO CHẨN ĐOÁN TỰ NHẬN THỨC COI
        </div>
        <div class="sub-title-text">AI DEPENDENCE INDEX REPORT</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  col_left, col_right = st.columns([1.1, 0.9])

  with col_left:
    st.markdown(f"### 👤 Học sinh: **{student_name}** ({grade})")

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

    st.markdown("#### 📢 Cảnh Báo Thị Giác Nhanh")
    if c_blind >= 0.5:
      st.error(
          f"🚨 **CẢNH BÁO SỬ DỤNG AI MÙ QUÁNG:** Bạn đã dành"
          f" **{c_blind*100:.0f}%** bài làm để chép từ AI mà không qua kiểm"
          " chứng phản biện! Hãy dừng ngay việc copy-paste để tránh tiêu biến"
          " tư duy độc lập."
      )
    else:
      st.info(
          f"💡 Tỷ lệ chấp nhận đáp án AI chưa qua kiểm định:"
          f" **{c_blind*100:.0f}%**."
      )

    if t_off <= 0.3:
      st.warning(
          f"⚠️ **CẢNH BÁO THỜI GIAN SUY NGHĨ T_off:** Chỉ số thời gian suy nghĩ"
          f" T_off của bạn hiện ở mức rất thấp (**{t_off:.2f}**). Bạn đang quá"
          " vội vã tìm kiếm 'lối tắt' thay vì tự nháp bài."
      )
    else:
      st.success(f"✅ Chỉ số nỗ lực tư duy T_off đạt mức tích cực: **{t_off:.2f}**.")

    st.markdown("#### 📐 Bảng Thông Số Chi Tiết")
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
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

  with col_right:
    st.markdown("### 📊 Biểu Đồ Radar Năng Lực Tự Chủ")

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

    fig, ax = plt.subplots(figsize=(4.8, 4.8), subplot_kw=dict(polar=True))
    color_code = (
        "#FF4B4B" if coi > 60 else ("#FFAA00" if coi >= 30 else "#00CC66")
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

    st.markdown(
        """
    <div class='note-box'>
    <b>💡 Hướng dẫn đọc biểu đồ Radar (Thang điểm 0 - 100%):</b><br>
    • <b>Mốc 0 - 100%:</b> Quy đổi toàn bộ về phần trăm (%). Tâm là <b>0%</b> (yếu nhất), vòng ngoài là <b>100%</b> (làm chủ hoàn hảo).<br>
    • <b>T_off:</b> Nỗ lực tư duy độc lập = T_off × 100%.<br>
    • <b>C_blind:</b> Màng lọc phản biện = (1 - C_blind) × 100%.<br>
    • <b>F_off:</b> Tính tự lực giải quyết = (1 - F_off) × 100%.<br>
    • <b>Metacognition:</b> Năng lực tự kiểm soát nhận thức = 100 - COI.<br>
    📌 <i><b>Quy tắc thị giác:</b> Diện tích phủ càng rộng, năng lực tự chủ tư duy càng toàn diện.</i>
    </div>
    """,
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.markdown("### 📝 ĐÁNH GIÁ TỰ NHẬN THỨC CHI TIẾT")

  if coi < 30:
    st.markdown(
        f"""
        <div class='eval-box status-success'>
        <h4>🟢 MỨC ĐỘ THẤP (COI = {coi:.2f}): NĂNG LỰC TỰ CHỦ & TƯ DUY ĐỘC LẬP TỐT</h4>
        • <b>Đánh giá tổng quan:</b> Học sinh thể hiện tinh thần tự chủ rất cao trong quá trình học tập. AI chỉ đóng vai trò là một công cụ hỗ trợ mở rộng kiến thức chứ không ảnh hưởng đến khả năng tư duy độc lập của học sinh.<br>
        • <b>Điểm mạnh:</b> Dành thời gian tự nháp và phân tích bài tập (T_off cao) trước khi tìm kiếm sự hỗ trợ từ công nghệ. Có tư duy phản biện tốt, duy trì thói quen kiểm tra và sàng lọc thông tin từ AI (C_blind thấp).<br>
        • <b>Khuyến nghị định hướng:</b> Tiếp tục duy trì phương pháp học tập chủ động hiện tại. Khuyến khích ứng dụng AI ở các cấp độ cao hơn như: phản biện ý tưởng, tối ưu hóa giải pháp hoặc sáng tạo dự án.
        </div>
        """,
        unsafe_allow_html=True,
    )
  elif coi <= 60:
    st.markdown(
        f"""
        <div class='eval-box status-warning'>
        <h4>🟡 MỨC ĐỘ TRUNG BÌNH (COI = {coi:.2f}): NGUY CƠ BẮT ĐẦU PHỤ THUỘC AI</h4>
        • <b>Đánh giá tổng quan:</b> Học sinh bắt đầu xuất hiện dấu hiệu phụ thuộc thói quen vào AI. Dù vẫn có khả năng tự làm bài, học sinh có xu hướng ngả sang việc tìm kiếm đáp án nhanh từ AI khi gặp các dạng bài khó hoặc áp lực thời gian.<br>
        • <b>Điểm cần lưu ý:</b> Tần suất hỏi AI (F_off) hoặc thời gian tự suy nghĩ (T_off) đang ở ngưỡng báo động, cho thấy sự thiếu kiên nhẫn khi đối mặt với bài tập phức tạp. Đôi khi còn chủ quan chấp nhận câu trả lời của AI mà chưa qua bước đối soát logic.<br>
        • <b>Khuyến nghị định hướng:</b> Áp dụng "Quy tắc 15 phút" - Bắt buộc tự suy nghĩ và viết nháp tối thiểu 15 phút trước khi tra cứu AI. Đổi thói quen đặt câu hỏi: Chỉ nhờ AI gợi ý phương pháp/khung ý tưởng, tuyệt đối không xin lời giải trực tiếp.
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"""
        <div class='eval-box status-danger'>
        <h4>🔴 MỨC ĐỘ CAO (COI = {coi:.2f}): CẢNH BÁO LẠM DỤNG & SUY GIẢM TƯ DUY</h4>
        • <b>Đánh giá tổng quan:</b> <b>Cảnh báo nghiêm trọng:</b> Học sinh đang lạm dụng AI ở mức độ cao. Hành vi này đang làm tiêu biến dần năng lực tư duy độc lập, kỹ năng giải quyết vấn đề và tư duy phản biện cá nhân.<br>
        • <b>Biểu hiện rủi ro:</b> Lập tức hỏi AI ngay khi nhận đề bài mà không trải qua quá trình tự suy nghĩ (T_off gần như bằng 0). Sao chép nguyên văn kết quả từ AI (C_blind cao), thụ động tin tưởng tuyệt đối vào máy móc mà không nhận diện được các lỗi ảo giác (hallucination) của AI.<br>
        • <b>Biện pháp can thiệp gấp:</b> Thực hiện "Thử thách Cai nghiện AI": Hoàn toàn không dùng AI trong 1–2 tuần đối với các bài tập về nhà để khôi phục thói quen tự tư duy. Yêu cầu nộp kèm bản nháp tay cùng với bài làm chính thức.
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.markdown("### 🎯 LỘ TRÌNH GAMIFICATION: 4 BƯỚC CHUYỂN HÓA TƯ DUY")
  st.write(
      "Thực hiện lần lượt các bước dưới đây từ trên xuống dưới để rèn luyện bản"
      " lĩnh tự học:"
  )

  st.markdown("##### 🟢 Level 1: Nỗ Lực Tư Duy Độc Lập (T_off)")
  st.checkbox(
      "Cam kết tự nháp và suy nghĩ tối thiểu 10–15 phút trước khi mở AI trợ"
      " giúp.",
      key="lvl1",
  )
  st.markdown("---")

  st.markdown(
      "##### 🟡 Level 2: Hỏi Định Hướng & Phương Pháp - Không Hỏi Đáp Án"
  )
  st.checkbox(
      "Tuyệt đối không xin đáp án trực tiếp. Chỉ yêu cầu AI hướng dẫn phương"
      " hướng, công thức và khung cách làm khi bị bế tắc.",
      key="lvl2",
  )
  st.markdown("---")

  st.markdown("##### 🟠 Level 3: Kiểm Chứng Phản Biện (C_blind)")
  st.checkbox(
      "Đóng vai người kiểm duyệt: Chủ động truy tìm ít nhất 1 lỗi logic hoặc"
      " bẫy ảo giác trong câu trả lời của AI.",
      key="lvl3",
  )
  st.markdown("---")

  st.markdown("##### 🔴 Level 4: Làm Chủ Công Nghệ Hoàn Toàn")
  st.checkbox(
      "Hoàn thành 1 bài tập phức tạp 100% bằng năng lực cá nhân, sau đó chỉ"
      " dùng AI đóng vai trò người phản biện chấm điểm.",
      key="lvl4",
  )
