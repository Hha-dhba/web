import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Sunnyx Cinema | Đỉnh Cao Điện Ảnh",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# ==========================================
# 2. KHỞI TẠO TRẠNG THÁI (SESSION STATE)
# ==========================================
if 'ad_closed' not in st.session_state: st.session_state.ad_closed = False
if 'is_logged_in' not in st.session_state: st.session_state.is_logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = 'guest'
if 'username' not in st.session_state: st.session_state.username = ''
if 'current_page' not in st.session_state: st.session_state.current_page = 'home' # home, booking, history
if 'selected_movie' not in st.session_state: st.session_state.selected_movie = ''

# Bộ nhớ tạm để lưu danh sách tài khoản dùng thử (Mock Database)
if 'registered_users' not in st.session_state: 
    st.session_state.registered_users = {'admin': '123'}

# ==========================================
# 3. HÀM CHUYỂN TRANG & POPUP QUẢNG CÁO
# ==========================================
def navigate_to(page, movie=""):
    st.session_state.current_page = page
    if movie: st.session_state.selected_movie = movie
    st.rerun()

@st.dialog("🔥 SIÊU PHẨM SẮP RA MẮT TẠI SUNNYX CINEMA", width="large")
def show_advertisement():
    st.markdown("<h3 style='text-align: center; color: #FFC107; margin-top:0; font-weight: 800;'>ĐÓN XEM BOM TẤN MÙA HÈ</h3>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070", use_column_width=True)
    st.markdown("<p style='text-align:center; color:#CCC; margin-top: 15px;'>Suất chiếu đặc biệt. Đặt vé ngay hôm nay để nhận combo bắp nước miễn phí!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("❌ ĐÓNG QUẢNG CÁO & VÀO RẠP", type="primary", use_container_width=True):
            st.session_state.ad_closed = True
            st.rerun()

# ==========================================
# 4. CSS DÀNH CHO GIAO DIỆN (Navy Dark)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    .stApp { background: #1B1E23; color: #E8EAED; }
    header {visibility: hidden;}

    .glass-effect {
        background: #252830; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px;
    }

    .nav-container {
        display: flex; justify-content: space-between; align-items: center; padding: 15px 30px;
        margin-bottom: 25px; background: #252830; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .nav-logo { font-size: 1.8rem; font-weight: 900; color: #FFF; margin: 0; text-transform: uppercase; letter-spacing: 1px;}
    .nav-logo span { color: #FFC107; cursor: pointer;}
    
    .hero-container {
        background-image: url('https://images.unsplash.com/photo-1533158307598-773428a39dbd?q=80&w=2070');
        background-size: cover; background-position: center 30%; height: 450px; border-radius: 20px;
        display: flex; flex-direction: column; justify-content: center; padding: 60px; margin-bottom: 40px;
        position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.1);
    }
    .hero-overlay {
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to right, rgba(27,30,35,0.95) 0%, rgba(27,30,35,0.7) 50%, rgba(27,30,35,0.2) 100%); z-index: 1;
    }
    .hero-content { position: relative; z-index: 2; max-width: 650px; }
    .hero-tag { color: #1B1E23; font-weight: 800; padding: 6px 12px; background: #FFC107; border-radius: 6px; margin-bottom: 15px; display: inline-block; text-transform: uppercase; font-size: 0.85rem;}
    .hero-title { font-size: 3.2rem; font-weight: 900; color: white; margin: 0 0 15px 0; text-transform: uppercase; line-height: 1.2;}
    .hero-desc { font-size: 1.1rem; color: #B0B3B8; margin-bottom: 25px; }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FFC107 0%, #FFB300 100%); color: #111 !important; 
        font-weight: 800; border: none; transition: all 0.3s; padding: 10px 0; border-radius: 8px;
    }
    .stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 193, 7, 0.4); }

    .movie-card {
        background: #252830; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08);
        overflow: hidden; transition: transform 0.3s, box-shadow 0.3s; height: 100%; margin-bottom: 15px;
    }
    .movie-card:hover { transform: translateY(-8px); box-shadow: 0 12px 24px rgba(0,0,0,0.5); border-color: rgba(255, 193, 7, 0.5); }
    .img-wrapper { width: 100%; aspect-ratio: 2 / 3; overflow: hidden; background-color: #111; }
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.5s; }
    .movie-card:hover .img-wrapper img { transform: scale(1.08); }
    .movie-info { padding: 15px; }
    .movie-title { font-size: 1.1rem; font-weight: 800; color: #FFF; margin: 0 0 8px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .movie-meta { font-size: 0.85rem; color: #9AA0A6; margin: 0 0 8px 0; }
    .movie-tags { display: flex; justify-content: space-between; align-items: center; }
    .movie-rating { color: #FFC107; font-weight: 800; font-size: 1rem; margin: 0;}
    
    /* Giao diện ghế ngồi */
    .seat { text-align: center; background: #3C4043; padding: 10px; border-radius: 8px; margin: 5px; cursor: pointer; color: white; font-weight:bold;}
    .seat-booked { background: #FF4B4B !important; color: white !important; cursor: not-allowed;}
    .seat-screen { background: #FFC107; text-align: center; color: black; font-weight: 900; padding: 5px; border-radius: 8px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR: ĐĂNG NHẬP / ĐĂNG KÝ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFC107;'>🔒 TÀI KHOẢN</h2>", unsafe_allow_html=True)
    
    if not st.session_state.is_logged_in:
        st.info("Vui lòng đăng nhập hệ thống.")
        
        # Tạo 2 Tabs cho Đăng nhập và Đăng ký
        tab_login, tab_register = st.tabs(["🔑 Đăng Nhập", "📝 Đăng Ký"])
        
        with tab_login:
            with st.form("login_form"):
                st.markdown("*(Gợi ý: Tài khoản `admin` - Mật khẩu `123`)*")
                username_input = st.text_input("Tên đăng nhập")
                password_input = st.text_input("Mật khẩu", type="password")
                submitted = st.form_submit_button("ĐĂNG NHẬP", type="primary")
                
                if submitted:
                    if username_input == "" or password_input == "":
                        st.error("Vui lòng nhập đủ thông tin!")
                    # Kiểm tra tài khoản trong mock database
                    elif username_input in st.session_state.registered_users and st.session_state.registered_users[username_input] == password_input:
                        st.session_state.is_logged_in = True
                        st.session_state.username = username_input
                        if username_input.lower() == 'admin':
                            st.session_state.user_role = "admin"
                            st.session_state.current_page = "admin_dash"
                        else:
                            st.session_state.user_role = "customer"
                            st.session_state.current_page = "home"
                        st.rerun()
                    else:
                        # Fallback cho tài khoản mặc định nhập bừa
                        if password_input == "123" and username_input != 'admin':
                            st.session_state.is_logged_in = True
                            st.session_state.username = username_input
                            st.session_state.user_role = "customer"
                            st.session_state.current_page = "home"
                            st.rerun()
                        else:
                            st.error("Tài khoản hoặc mật khẩu không đúng!")
        
        with tab_register:
            with st.form("register_form"):
                st.markdown("Tạo tài khoản Khách hàng mới")
                new_username = st.text_input("Tên đăng nhập mới")
                new_password = st.text_input("Mật khẩu", type="password")
                confirm_password = st.text_input("Xác nhận mật khẩu", type="password")
                reg_submitted = st.form_submit_button("ĐĂNG KÝ", type="primary")
                
                if reg_submitted:
                    if new_username == "" or new_password == "":
                        st.error("Vui lòng nhập đầy đủ thông tin!")
                    elif new_password != confirm_password:
                        st.error("Mật khẩu xác nhận không khớp!")
                    elif new_username in st.session_state.registered_users:
                        st.error("Tên đăng nhập đã tồn tại! Vui lòng chọn tên khác.")
                    else:
                        st.session_state.registered_users[new_username] = new_password
                        st.success("🎉 Đăng ký thành công! Chuyển sang tab Đăng Nhập để vào rạp nhé.")
                        
    else:
        st.success(f"👋 Xin chào, **{st.session_state.username}**!")
        st.caption(f"Vai trò: {st.session_state.user_role.upper()}")
        
        if st.session_state.user_role == 'customer':
            if st.button("🏠 Trang chủ Phim", use_container_width=True): navigate_to("home")
            if st.button("🎫 Lịch sử vé của tôi", use_container_width=True): navigate_to("history")
            st.divider()
            
        if st.button("ĐĂNG XUẤT", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.user_role = 'guest'
            st.session_state.username = ''
            st.session_state.current_page = 'home'
            st.rerun()

# ==========================================
# 6. KHUNG GIAO DIỆN CHÍNH
# ==========================================
st.markdown("""
<div class="nav-container">
    <div class="nav-logo">☀️ SUNNYX <span>CINEMA</span></div>
    <div style="color: #FFC107; font-weight: bold;">📍 CƠ SỞ DUY NHẤT: SUNNYX CENTER</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# A. GIAO DIỆN QUẢN TRỊ VIÊN (ADMIN DASHBOARD)
# ------------------------------------------
if st.session_state.user_role == 'admin':
    st.markdown("## ⚙️ BẢNG ĐIỀU KHIỂN QUẢN TRỊ")
    
    # Chỉ số nhanh
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng Doanh Thu", "45.000.000 đ", "+15%")
    c2.metric("Vé Đã Bán (Hôm nay)", "320 vé", "+24")
    c3.metric("Phim Đang Chiếu", "8 phim", "0")
    c4.metric("Khách Hàng Mới", "45", "+5")
    
    st.divider()
    
    tab_movies, tab_showtimes, tab_rooms = st.tabs(["🎬 Quản lý Phim", "⏰ Lịch Chiếu", "🏢 Sơ đồ Phòng"])
    
    with tab_movies:
        col_list, col_add = st.columns([2, 1])
        with col_list:
            st.subheader("Danh sách Phim (movies.csv)")
            df_movies = pd.DataFrame({
                "Mã Phim": ["M01", "M02", "M03", "M04"],
                "Tên Phim": ["Dune: Hành Tinh Cát 2", "Kung Fu Panda 4", "Godzilla x Kong", "Exhuma: Quật Mộ"],
                "Thời lượng": ["166p", "94p", "115p", "134p"],
                "Trạng thái": ["Đang chiếu", "Đang chiếu", "Sắp chiếu", "Đang chiếu"]
            })
            st.dataframe(df_movies, use_container_width=True, hide_index=True)
            
        with col_add:
            st.subheader("Thêm Phim Mới")
            with st.form("admin_add_movie"):
                st.text_input("Tên phim (*)")
                st.text_input("Thể loại")
                st.number_input("Thời lượng (phút)", min_value=1)
                st.selectbox("Độ tuổi", ["P (Mọi lứa tuổi)", "T13", "T16", "T18"])
                if st.form_submit_button("LƯU PHIM", type="primary"):
                    st.success("Tích hợp lưu vào movies.csv thành công!")

    with tab_showtimes:
        st.subheader("Quản lý Suất Chiếu (showtimes.csv)")
        with st.form("add_showtime"):
            c1, c2, c3 = st.columns(3)
            with c1: st.selectbox("Chọn Phim", ["Dune: Hành Tinh Cát 2", "Kung Fu Panda 4"])
            with c2: st.selectbox("Chọn Phòng", ["Phòng 01 (IMAX)", "Phòng 02 (3D)", "Phòng 03 (Standard)"])
            with c3: st.time_input("Giờ chiếu")
            if st.form_submit_button("TẠO SUẤT CHIẾU", type="primary"):
                st.success("Tích hợp lưu vào showtimes.csv thành công!")

    with tab_rooms:
        st.subheader("Danh sách Phòng chiếu tại Sunnyx Center (rooms.csv)")
        df_rooms = pd.DataFrame({
            "Mã Phòng": ["R01", "R02", "R03"],
            "Tên Phòng": ["IMAX 01", "3D 02", "Standard 03"],
            "Số Lượng Ghế": [120, 80, 50],
            "Tình Trạng": ["Đang hoạt động", "Đang hoạt động", "Bảo trì"]
        })
        st.dataframe(df_rooms, use_container_width=True, hide_index=True)

# ------------------------------------------
# B. GIAO DIỆN KHÁCH HÀNG - TRANG CHỦ
# ------------------------------------------
elif st.session_state.current_page == 'home':
    # Banner
    st.markdown("""
    <div class="hero-container">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-tag">⚡ ĐỘC QUYỀN TẠI SUNNYX</div>
            <div class="hero-title">DUNE: HÀNH TINH CÁT 2</div>
            <div class="hero-desc">Trải nghiệm âm thanh và hình ảnh sống động nhất tại cơ sở Sunnyx duy nhất của chúng tôi.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Đặt vé nhanh
    with st.container():
        st.markdown('<div class="glass-effect" style="padding: 25px; margin-top: -30px; margin-bottom:30px; position:relative; z-index:10;">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#FFC107; margin-top:0;'>🎟️ TÌM SUẤT CHIẾU NHANH</h4>", unsafe_allow_html=True)
        
        qb1, qb2, qb3, qb4 = st.columns([2, 1, 1, 1])
        with qb1: st.selectbox("Chọn Phim", ["Dune: Hành Tinh Cát 2", "Kungfu Panda 4", "Godzilla x Kong", "Exhuma: Quật Mộ"])
        with qb2: st.selectbox("Ngày Xem", ["Hôm nay", "Ngày mai"])
        with qb3: st.selectbox("Suất Chiếu", ["09:30 (IMAX)", "13:15 (3D)", "20:30 (2D)"])
        with qb4: 
            st.write("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
            if st.button("CHỌN GHẾ NGAY", type="primary", use_container_width=True):
                if not st.session_state.is_logged_in:
                    st.error("⚠️ Vui lòng đăng nhập để đặt vé!")
                else:
                    navigate_to("booking", "Dune: Hành Tinh Cát 2")
            st.write("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Danh sách phim
    st.markdown("<h3 style='margin-bottom: 20px;'>🔥 DANH SÁCH PHIM ĐANG CHIẾU</h3>", unsafe_allow_html=True)
    cols = st.columns(4)
    
    def create_premium_movie_card(col, title, genre, duration, age, rating, img_url):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <div class="img-wrapper"><img src="{img_url}"></div>
                <div class="movie-info">
                    <p class="movie-title">{title}</p>
                    <p class="movie-meta">{genre} • {duration}</p>
                    <div class="movie-tags">
                        <p class="movie-rating">⭐ {rating}</p>
                        <span style="background: #3C4043; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;">{age}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🎫 MUA VÉ", key=f"btn_{title}", use_container_width=True, type="primary"):
                if not st.session_state.is_logged_in:
                    st.error(f"⚠️ Vui lòng đăng nhập để đặt vé phim {title}!")
                else:
                    navigate_to("booking", title)

    create_premium_movie_card(cols[0], "Dune: Hành Tinh Cát 2", "Viễn tưởng", "166 phút", "T13", "9.5", "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&q=80")
    create_premium_movie_card(cols[1], "Kung Fu Panda 4", "Hoạt hình", "94 phút", "P", "8.9", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80")
    create_premium_movie_card(cols[2], "Godzilla x Kong", "Hành động", "115 phút", "T13", "9.0", "https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=500&q=80")
    create_premium_movie_card(cols[3], "Exhuma: Quật Mộ", "Kinh dị", "134 phút", "T16", "9.2", "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=500&q=80")

# ------------------------------------------
# C. GIAO DIỆN KHÁCH HÀNG - ĐẶT GHẾ (BOOKING)
# ------------------------------------------
elif st.session_state.current_page == 'booking':
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"): navigate_to("home")
    
    st.markdown(f"## 🎫 ĐẶT VÉ: {st.session_state.selected_movie}")
    st.info("📍 Địa điểm: Sunnyx Cinema Center | 🎬 Phòng: IMAX 01 | ⏰ Suất: 20:30 - Hôm nay")
    
    st.markdown('<div class="seat-screen">MÀN HÌNH CHÍNH</div>', unsafe_allow_html=True)
    
    # Giao diện chọn ghế mô phỏng (A, B, C, D)
    seat_rows = ['A', 'B', 'C', 'D']
    selected_seats = []
    
    for row in seat_rows:
        cols = st.columns(8)
        for i, col in enumerate(cols):
            seat_name = f"{row}{i+1}"
            with col:
                # Mô phỏng ghế ngẫu nhiên đã bị người khác đặt
                is_booked = (hash(seat_name) % 5 == 0) 
                
                if is_booked:
                    st.button(seat_name, key=f"seat_{seat_name}", disabled=True)
                else:
                    # Dùng checkbox để chọn ghế cho dễ thao tác trong Streamlit
                    if st.checkbox(seat_name, key=f"chk_{seat_name}"):
                        selected_seats.append(seat_name)
                        
    st.divider()
    col_sum1, col_sum2 = st.columns([3, 1])
    with col_sum1:
        st.markdown(f"**Ghế bạn đang chọn:** {', '.join(selected_seats) if selected_seats else 'Chưa chọn ghế'}")
        st.markdown(f"**Tổng tiền:** {len(selected_seats) * 85000:,} VNĐ (85.000đ/vé)")
    with col_sum2:
        if st.button("XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True, disabled=len(selected_seats)==0):
            st.success("Thanh toán thành công! Vé đã được lưu vào Lịch sử (tickets.csv).")
            # Tích hợp booking_controller để lưu file tickets.csv

# ------------------------------------------
# D. GIAO DIỆN KHÁCH HÀNG - LỊCH SỬ VÉ
# ------------------------------------------
elif st.session_state.current_page == 'history':
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"): navigate_to("home")
    
    st.markdown("## 🎫 LỊCH SỬ ĐẶT VÉ CỦA TÔI")
    st.write("Tích hợp controller để đọc từ tickets.csv và lọc theo tên đăng nhập hiện tại.")
    
    # Mock data lịch sử
    df_history = pd.DataFrame({
        "Mã Vé": ["TK0912", "TK0844"],
        "Tên Phim": ["Kung Fu Panda 4", "Dune: Hành Tinh Cát 2"],
        "Ghế": ["C4, C5", "F10"],
        "Ngày Chiếu": ["20/05/2026", "15/05/2026"],
        "Tổng tiền": ["170.000 đ", "95.000 đ"],
        "Trạng thái": ["Đã xem", "Đã xem"]
    })
    st.dataframe(df_history, use_container_width=True, hide_index=True)

# ==========================================
# 7. GỌI HIỂN THỊ QUẢNG CÁO TẠI TRANG CHỦ
# ==========================================
if not st.session_state.ad_closed and st.session_state.current_page == 'home' and st.session_state.user_role != 'admin':
    show_advertisement()