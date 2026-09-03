import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. THIẾT LẬP CẤU HÌNH WEB APP CHUYÊN NGHIỆP
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Chẩn Đoán Tư Duy COI",
    page_icon="⚡",
    layout="wide",
)

# Style CSS tinh chỉnh Font chữ & Giao diện Đẹp
st.markdown(
    """
    <style>
    /* NHẬP FONT CHỮ HIỆN ĐẠI TỪ GOOGLE FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Font mặc định cho toàn bộ ứng dụng */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #F8FAFC;
        color: #1E293B;
    }
    
    /* Cấu hình Typography cho các thẻ Tiêu đề Streamlit */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em !important;
    }

    /* Header Banner sáng & đẹp */
    .app-header {
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%);
        padding: 32px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3);
        text-align: center;
        margin-bottom: 28px;
        color: #FFFFFF;
    }
    .app-header-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0;
        text-transform: uppercase;
        line-height: 1.2;
        text-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    .app-header-subtitle {
        font-family: 'Inter', sans-serif !important;
        color: #E0F2FE;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 2.5px;
        margin-top: 8px;
        text-transform: uppercase;
    }
    
    /* Style cho Nút Bấm Chuyển Trang & Tương Tác */
    div.stButton > button {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        border-radius: 14px !important;
        height: 3.4em !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
        font-size: 16px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(37, 99, 235, 0.45) !important;
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    }

    /* Thẻ trạng thái kết quả */
    .status-card {
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        font-weight: 700;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .status-danger { background-color: #FEF2F2; color: #991B1B; border: 1.5px solid #FCA5A5; }
    .status-warning { background-color: #FFFBEB; color: #92400E; border: 1.5px solid #FCD34D; }
    .status-success { background-color: #F0FDF4; color: #166534; border: 1.5px solid #86EFAC; }
    
    /* Khối đánh giá chi tiết */
    .eval-box {
        padding: 26px;
        border-radius: 16px;
        margin-top: 18px;
        line-height: 1.8;
        font-size: 15px;
    }
    .eval-box h4 {
        margin-top: 0;
        margin-bottom: 16px;
        font-size: 19px;
        font-weight: 800;
    }
    .eval-section-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        margin-top: 12px;
        display: block;
        font-size: 15.5px;
    }

    /* Hướng dẫn đọc Biểu đồ Radar đặt dưới cột trái */
    .radar-guide-container {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 22px;
        margin-top: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
    }
    .radar-guide-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16.5px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .radar-main-tip {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 14px;
        color: #1E40AF;
        font-weight: 600;
        margin-bottom: 16px;
        line-height: 1.5;
    }
    .radar-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .radar-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px;
        transition: all 0.2s ease;
    }
    .radar-card:hover {
        border-color: #94A3B8;
        background: #F1F5F9;
    }
    .radar-card-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 13.5px;
        color: #0F172A;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .radar-card-desc {
        font-size: 12.5px;
        color: #475569;
        line-height: 1.5;
    }

    /* Thẻ Lộ trình Gamification */
    .level-card {
        padding: 20px 22px;
        border-radius: 14px;
        margin-top: 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .level-card-easy { border-left: 6px solid #10B981; background: #ECFDF5; }
    .level-card-medium { border-left: 6px solid #F59E0B; background: #FFFBEB; }
    .level-card-hard { border-left: 6px solid #F97316; background: #FFF7ED; }
    .level-card-expert { border-left: 6px solid #EF4444; background: #FEF2F2; }

    .level-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 16.5px;
        margin-bottom: 8px;
    }
    .level-desc {
        font-size: 14.5px;
        color: #334155;
        line-height: 1.7;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Khởi tạo Session State quản lý chuyển trang
if "page" not in st.session_state:
  st.session_state.page = 1

# ==========================================
# TRANG 1: NHẬP THÔNG TIN VÀ CHỈ SỐ HÀNH VI
# ==========================================
if st.session_state.page == 1:
  st.markdown(
      """
    <div class="app-header">
        <div class="app-header-title">PHIẾU CHẨN ĐOÁN TƯ DUY CÁ NHÂN</div>
        <div class="app-header-subtitle">PERSONAL AI-DEPENDENCE CHECK</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  col_center1, col_center2, col_center3 = st.columns([1, 2.5, 1])

  with col_center2:
    st.subheader("📋 Bước 1: Thông tin học sinh")
    student_name = st.text_input(
        "Họ và tên học sinh:",
        st.session_state.get("student_name", "Nguyễn Văn A"),
        placeholder="Nhập đầy đủ họ tên...",
    )
    grade = st.selectbox(
        "Khối lớp:",
        ["Khối 10", "Khối 11", "Khối 12"],
        index=["Khối 10", "Khối 11", "Khối 12"].index(
            st.session_state.get("grade", "Khối 10")
        ),
    )

    st.markdown("---")
    st.subheader("⚙️ Bước 2: Nhập chỉ số hành vi thực nghiệm")

    c_blind = st.slider(
        "1. Tỷ lệ sao chép mù quáng (C_blind):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("c_blind", 0.4), 1),
        step=0.1,
        format="%.1f",
        help="Tỷ lệ bài làm chép nguyên văn từ AI không qua kiểm chứng",
    )

    f_off = st.slider(
        "2. Tần suất cầu viện AI (F_off):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("f_off", 0.6), 1),
        step=0.1,
        format="%.1f",
        help="Tỷ lệ câu hỏi gửi lệnh cho AI xử lý",
    )

    t_off = st.slider(
        "3. Thời gian suy nghĩ độc lập (T_off):",
        min_value=0.0,
        max_value=1.0,
        value=round(st.session_state.get("t_off", 0.17), 2),
        step=0.01,
        format="%.2f",
        help="Chỉ số thời gian/nỗ lực suy nghĩ trước khi hỏi AI",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(
        "🚀 XUẤT BÁO CÁO PHÂN TÍCH & ĐÁNH GIÁ CHUYÊN SÂU",
        use_container_width=True,
    ):
      st.session_state.student_name = student_name
      st.session_state.grade = grade
      st.session_state.c_blind = c_blind
      st.session_state.f_off = f_off
      st.session_state.t_off = t_off

      st.session_state.page = 2
      st.rerun()

# ==========================================
# TRANG 2: BÁO CÁO KẾT QUẢ & LỘ TRÌNH CHUYÊN SÂU
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

  if st.button("⬅️ Quay lại trang nhập thông số"):
    st.session_state.page = 1
    st.rerun()

  # ---------------- 1. KHỐI TRUNG TÂM (ĐẶT Ở GIỮA TRANG) ----------------
  st.markdown(f"### 👤 Hồ sơ: **{student_name}** ({grade})")

  m1, m2 = st.columns([1, 1])
  with m1:
    st.metric(label="Chỉ số Phụ thuộc AI (COI)", value=f"{coi} / 100")
  with m2:
    if coi > 60:
      st.markdown(
          """
              <div class='status-card status-danger'>
                  <div style='font-size: 16px;'>MỨC ĐỘ: CAO 🚨</div>
                  <small>Cảnh báo lạm dụng nghiêm trọng</small>
              </div>
              """,
          unsafe_allow_html=True,
      )
    elif coi >= 30:
      st.markdown(
          """
              <div class='status-card status-warning'>
                  <div style='font-size: 16px;'>MỨC ĐỘ: TRUNG BÌNH ⚠️</div>
                  <small>Có nguy cơ bắt đầu phụ thuộc</small>
              </div>
              """,
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          """
              <div class='status-card status-success'>
                  <div style='font-size: 16px;'>MỨC ĐỘ: THẤP ✅</div>
                  <small>Năng lực tự chủ tư duy tốt</small>
              </div>
              """,
          unsafe_allow_html=True,
      )

  # Cảnh báo thị giác nhanh ở vị trí trung tâm rộng
  st.markdown("#### 📢 Cảnh Báo Thị Giác Nhanh")
  if c_blind >= 0.5:
    st.error(
        f"🚨 **CẢNH BÁO SAO CHÉP MÙ QUÁNG:** Bạn đã dành đến"
        f" **{c_blind*100:.0f}%** khối lượng bài làm để chép từ AI mà không qua"
        " kiểm chứng phản biện!"
    )
  else:
    st.info(
        f"💡 Tỷ lệ chấp nhận đáp án AI chưa qua kiểm định: **{c_blind*100:.0f}%**."
    )

  if t_off <= 0.3:
    st.warning(
        f"⚠️ **CẢNH BÁO THỜI GIAN SUY NGHĨ T_off:** Chỉ số nỗ lực tư duy của bạn"
        f" ở mức rất thấp (**{t_off:.2f}**). Hãy dành nhiều thời gian nháp độc"
        " lập hơn."
    )
  else:
    st.success(f"✅ Chỉ số nỗ lực tư duy T_off đạt mức tích cực: **{t_off:.2f}**.")

  st.markdown("<br>", unsafe_allow_html=True)

  # ---------------- 2. BỐ CỤC 2 CỘT CÂN BẰNG PHÍA DƯỚI ----------------
  col_left, col_right = st.columns([1, 1], gap="large")

  # CỘT TRÁI: BẢNG BÁO CÁO CHI TIẾT + HƯỚNG DẪN ĐỌC BIỂU ĐỒ
  with col_left:
    st.markdown("#### 📐 Bảng Báo Cáo Chi Tiết Thông Số")
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
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    # KHỐI HƯỚNG DẪN XEM BIỂU ĐỒ RADAR
    st.markdown(
        """
        <div class="radar-guide-container">
            <div class="radar-guide-header">
                🧭 HƯỚNG DẪN ĐỌC BIỂU ĐỒ RADAR
            </div>
            <div class="radar-main-tip">
                🎯 <b>Mẹo nhanh:</b> Vùng màu phủ càng <b>RỘNG & MỞ RỘNG RA RÌA</b> ➔ Năng lực tự chủ tư duy và kiểm soát AI của bạn càng cao!
            </div>
            <div class="radar-grid">
                <div class="radar-card">
                    <div class="radar-card-title">🧠 T_off (Nỗ lực tư duy)</div>
                    <div class="radar-card-desc">Càng xa tâm thể hiện sự kiên trì tự nháp & suy nghĩ trước khi mở AI.</div>
                </div>
                <div class="radar-card">
                    <div class="radar-card-title">🛡️ C_blind (Màng lọc phản biện)</div>
                    <div class="radar-card-desc">Càng xa tâm thể hiện khả năng chủ động đối soát, soi lỗi đáp án AI.</div>
                </div>
                <div class="radar-card">
                    <div class="radar-card-title">💪 F_off (Tính tự lực)</div>
                    <div class="radar-card-desc">Càng xa tâm thể hiện mức độ tự lực làm bài mà không ỷ lại vào AI.</div>
                </div>
                <div class="radar-card">
                    <div class="radar-card-title">👁️ Metacognition (Siêu nhận thức)</div>
                    <div class="radar-card-desc">Mức độ chủ động điều phối và kiểm soát hành vi học tập cá nhân.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  # CỘT PHẢI: BIỂU ĐỒ RADAR
  with col_right:
    st.markdown("#### 📊 Biểu Đồ Radar Năng Lực Tự Chủ")

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

    # Áp dụng Font chữ thống nhất cho Biểu đồ Matplotlib
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(5.4, 5.4), subplot_kw=dict(polar=True))
    color_code = (
        "#EF4444" if coi > 60 else ("#F59E0B" if coi >= 30 else "#10B981")
    )

    ax.plot(angles, stats, color=color_code, linewidth=2.5, linestyle="solid")
    ax.fill(angles, stats, color=color_code, alpha=0.25)
    ax.set_thetagrids(
        np.degrees(angles[:-1]), labels, fontsize=9.5, fontweight="bold"
    )

    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(
        ["0", "20", "40", "60", "80", "100"], fontsize=8, color="#64748B"
    )

    st.pyplot(fig)

  st.markdown("---")

  # ==========================================
  # PHẦN ĐÁNH GIÁ TỰ NHẬN THỨC CHI TIẾT
  # ==========================================
  st.markdown("### 📝 ĐÁNH GIÁ TỰ NHẬN THỨC CHI TIẾT")

  if coi < 30:
    st.markdown(
        f"""
        <div class='eval-box status-success'>
        <h4>🟢 MỨC ĐỘ THẤP (COI = {coi:.2f}): TỰ CHỦ CHỦ ĐỘNG & TƯ DUY ĐỘC LẬP TỐT</h4>
        <span class='eval-section-title'>📌 Thực trạng hành vi:</span>
        Học sinh thể hiện tinh thần tự học xuất sắc và bản lĩnh vững vàng trong quá trình giải quyết vấn đề. Trí tuệ nhân tạo (AI) chỉ đóng vai trò là một công cụ hỗ trợ tham khảo nâng cao, hoàn toàn không làm ảnh hưởng hay thay thế tư duy cá nhân.<br><br>
        <span class='eval-section-title'>💪 Điểm mạnh cốt lõi:</span>
        • Luôn dành khoảng thời gian thích đáng để tự đọc đề, phân tích và nháp lời giải trước khi tra cứu AI (chỉ số T_off cao).<br>
        • Duy trì thái độ hoài nghi khoa học, chủ động kiểm định và đối soát logic thông tin do AI cung cấp thay vì chấp nhận ngay (chỉ số C_blind rất thấp).<br><br>
        <span class='eval-section-title'>🚀 Định hướng phát triển:</span>
        Tiếp tục duy trì thói quen tích cực này. Học sinh có thể nâng cấp việc sử dụng AI lên các mức độ cao hơn như: dùng AI để phản biện chéo các lập luận cá nhân, tìm kiếm giải pháp tối ưu hơn cho bài toán hoặc mở rộng góc nhìn chuyên sâu.
        </div>
        """,
        unsafe_allow_html=True,
    )
  elif coi <= 60:
    st.markdown(
        f"""
        <div class='eval-box status-warning'>
        <h4>🟡 MỨC ĐỘ TRUNG BÌNH (COI = {coi:.2f}): CẢNH BÁO NGUY CƠ BẮT ĐẦU PHỤ THUỘC</h4>
        <span class='eval-section-title'>📌 Thực trạng hành vi:</span>
        Học sinh bắt đầu hình thành thói quen ngả lưng vào sự trợ giúp của AI. Dù bản thân vẫn có năng lực tự làm bài, nhưng khi đối mặt với các dạng bài phức tạp, bài tập dài hoặc áp lực thời gian, học sinh thường chọn cách tra cứu AI ngay để lấy đáp án nhanh.<br><br>
        <span class='eval-section-title'>⚠️ Yếu tố rủi ro:</span>
        • Thời gian tự suy nghĩ độc lập (T_off) đang bị rút ngắn đáng kể, cho thấy sự giảm sút về độ kiên trì khi giải quyết vấn đề khó.<br>
        • Đôi khi chủ quan sao chép lời giải của AI mà bỏ qua bước đối chiếu logic, dễ dẫn đến việc tiếp thu kiến thức sai lệch do lỗi "ảo giác" (hallucination) của máy tính.<br><br>
        <span class='eval-section-title'>💡 Khuyến nghị điều chỉnh:</span>
        Áp dụng nghiêm túc "Quy tắc 15 phút" - Bắt buộc tự nháp và tìm phương án tối thiểu 15 phút trước khi mở AI. Đổi cách tương tác: Chỉ xin AI gợi ý hướng đi hoặc dàn ý, tuyệt đối không yêu cầu tạo ra lời giải hoàn chỉnh.
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"""
        <div class='eval-box status-danger'>
        <h4>🔴 MỨC ĐỘ CAO (COI = {coi:.2f}): BÁO ĐỘNG LẠM DỤNG & SUY GIẢM NĂNG LỰC TƯ DUY</h4>
        <span class='eval-section-title'>🚨 Cảnh báo nghiêm trọng:</span>
        Học sinh đang phụ thuộc nghiêm trọng vào công cụ AI. Việc ủy thác toàn bộ bộ não cho máy tính xử lý đang khiến các phản xạ tư duy tự nhiên, kỹ năng phân tích và tư duy phản biện bị tiêu biến rõ rệt theo thời gian.<br><br>
        <span class='eval-section-title'>❌ Biểu hiện lâm sàng:</span>
        • Vừa nhận bài tập liền lập tức sao chép câu hỏi gửi cho AI (T_off gần như bằng 0).<br>
        • Lấy nguyên văn kết quả do AI tạo ra dán vào bài nộp (C_blind chạm ngưỡng báo động) mà không cần hiểu bản chất lời giải.<br>
        • Mất hoàn toàn màng lọc phản biện, thụ động tin tưởng 100% vào AI.<br><br>
        <span class='eval-section-title'>🛠️ Biện pháp can thiệp cấp bách:</span>
        Thực hiện "Thử thách cai nghiện AI" trong 2 tuần: Hoàn toàn không sử dụng AI khi làm bài tập về nhà để kích hoạt lại năng lực tự duy. Bắt buộc nộp kèm tờ giấy nháp tay có chữ ký kiểm duyệt đối với mọi bài làm.
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")

  # ==========================================
  # LỘ TRÌNH GAMIFICATION TỪ DỄ ĐẾN KHÓ
  # ==========================================
  st.markdown("### 🎯 LỘ TRÌNH TỰ RÈN LUYỆN TƯ DUY (GAMIFICATION)")
  st.write(
      "Thực hiện lần lượt các cấp độ bên dưới theo thứ tự từ **Dễ đến Khó** để"
      " từng bước làm chủ tư duy:"
  )

  st.markdown(
      """
    <div class="level-card level-card-easy">
        <div class="level-title">🟢 LEVEL 1 (MỨC DỄ): Cam Kết Thời Gian Nháp Độc Lập</div>
        <div class="level-desc">
            • <b>Mục tiêu:</b> Khôi phục thói quen tự suy nghĩ trước khi cầu viện công nghệ.<br>
            • <b>Hành động:</b> Bắt buộc cầm bút tự viết nháp và tìm phương án giải quyết tối thiểu <b>10 – 15 phút</b> đối với mỗi câu hỏi. Chỉ được phép mở AI sau khi đã có bản nháp cá nhân.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.checkbox("Đã hoàn thành Level 1", key="chk_lvl1")

  st.markdown(
      """
    <div class="level-card level-card-medium">
        <div class="level-title">🟡 LEVEL 2 (MỨC TRUNG BÌNH): Học Cách Đặt Câu Hỏi Định Hướng</div>
        <div class="level-desc">
            • <b>Mục tiêu:</b> Chuyển đổi AI từ "máy làm hộ" thành "trợ lý gợi ý".<br>
            • <b>Hành động:</b> Tuyệt đối không yêu cầu AI cung cấp lời giải hay đáp án trực tiếp. Chỉ đặt câu hỏi xin: <i>Công thức áp dụng, gợi ý các bước thực hiện, hoặc dàn ý tổng quan</i>.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.checkbox("Đã hoàn thành Level 2", key="chk_lvl2")

  st.markdown(
      """
    <div class="level-card level-card-hard">
        <div class="level-title">🟠 LEVEL 3 (MỨC KHÓ): Nhập Vai Người Kiểm Duyệt Phản Biện</div>
        <div class="level-desc">
            • <b>Mục tiêu:</b> Rèn luyện màng lọc tư duy khoa học (C_blind).<br>
            • <b>Hành động:</b> Đặt mình vào vị trí giám khảo: Khi nhận câu trả lời từ AI, chủ động truy tìm ít nhất <b>1 điểm nghi vấn, lỗi logic hoặc bẫy sai sót</b> trước khi chấp nhận thông tin.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.checkbox("Đã hoàn thành Level 3", key="chk_lvl3")

  st.markdown(
      """
    <div class="level-card level-card-expert">
        <div class="level-title">🔴 LEVEL 4 (MỨC NÂNG CAO): Làm Chủ Công Nghệ Hoàn Toàn</div>
        <div class="level-desc">
            • <b>Mục tiêu:</b> Khẳng định năng lực tự chủ tư duy tuyệt đối.<br>
            • <b>Hành động:</b> Hoàn thành 100% một bài tập khó hoàn toàn bằng sức mình. Sau đó gửi bài của mình cho AI và giao lệnh: <i>"Hãy phản biện và tìm điểm chưa tối ưu trong bài làm này của tôi"</i>.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.checkbox("Đã hoàn thành Level 4", key="chk_lvl4")
