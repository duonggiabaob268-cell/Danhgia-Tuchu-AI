# ==========================================
# TRANG 1: NHẬP THÔNG TIN VÀ CHỈ SỐ
# ==========================================
if st.session_state.page == 1:
  st.markdown(
      "<div class='main-title'>🔬 PHIẾU CHẨN ĐOÁN TƯ DUY CÁ NHÂN (PERSONAL"
      " AI-HEALTH CHECK)</div>",
      unsafe_allow_html=True,
  )

  col_center1, col_center2, col_center3 = st.columns([1, 2, 1])

  with col_center2:
    # Đã bỏ "Bước 1:"
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
    # Đã bỏ "Bước 2:"
    st.markdown("### ⚙️ Nhập các chỉ số hành vi thực nghiệm")

    # Cấu hình thanh kéo nhảy bước 0.1 và định dạng 1 chữ số thập phân (0.1, 0.2,... 1.0)
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
        value=round(st.session_state.get("t_off", 0.2), 1),
        step=0.1,
        format="%.1f",
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
