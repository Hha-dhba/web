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

# Thêm biến lưu trữ các ghế đang chọn
if 'selected_seats' not in st.session_state: st.session_state.selected_seats = []

# Bộ nhớ tạm để lưu danh sách tài khoản dùng thử (Mock Database)
if 'registered_users' not in st.session_state: 
    st.session_state.registered_users = {'admin': '123'}

# ==========================================
# 3. HÀM CHUYỂN TRANG & POPUP QUẢNG CÁO
# ==========================================
def navigate_to(page, movie=""):
    st.session_state.current_page = page
    if movie: 
        st.session_state.selected_movie = movie
        st.session_state.selected_seats = [] # Reset ghế khi đổi phim mới
    st.rerun()

@st.dialog("🔥 SIÊU PHẨM SẮP RA MẮT TẠI SUNNYX CINEMA", width="large")
def show_advertisement():
    st.markdown("<h3 style='text-align: center; color: #E71A0F; margin-top:0; font-weight: 800;'>ĐÓN XEM BOM TẤN MÙA HÈ</h3>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070", use_column_width=True)
    st.markdown("<p style='text-align:center; color:#555; margin-top: 15px;'>Suất chiếu đặc biệt. Đặt vé ngay hôm nay để nhận combo bắp nước miễn phí!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("❌ ĐÓNG QUẢNG CÁO", type="primary", use_container_width=True):
            st.session_state.ad_closed = True
            st.rerun()

# ==========================================
# 4. CSS DÀNH CHO GIAO DIỆN (Phong cách CGV - Light & Red)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    /* Giao diện nền sáng màu Kem (Cream) giống CGV */
    .stApp { background-color: #FDFCF0; color: #333333; }
    header {visibility: hidden;}

    /* Khung viền chung */
    .glass-effect {
        background: #FFFFFF; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #EBEBEB; border-radius: 8px;
    }

    /* Thanh điều hướng */
    .nav-container {
        display: flex; justify-content: space-between; align-items: center; padding: 15px 30px;
        margin-bottom: 25px; background: #FDFCF0; 
        border-top: 3px solid #E71A0F; border-bottom: 3px solid #E71A0F;
    }
    .nav-logo { font-size: 2.2rem; font-weight: 900; color: #E71A0F; margin: 0; text-transform: uppercase; letter-spacing: -1px;}
    .nav-logo span { color: #333333; font-size: 1.2rem; letter-spacing: 2px;}
    
    /* Banner */
    .hero-container {
        background-image: url('https://images.unsplash.com/photo-1533158307598-773428a39dbd?q=80&w=2070');
        background-size: cover; background-position: center 30%; height: 400px; border-radius: 8px;
        display: flex; flex-direction: column; justify-content: center; padding: 60px; margin-bottom: 40px;
        position: relative; overflow: hidden;
    }
    .hero-overlay {
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to right, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0.1) 100%); z-index: 1;
    }
    .hero-content { position: relative; z-index: 2; max-width: 650px; }
    .hero-tag { color: white; font-weight: 800; padding: 6px 12px; background: #E71A0F; border-radius: 4px; margin-bottom: 15px; display: inline-block; text-transform: uppercase; font-size: 0.85rem;}
    .hero-title { font-size: 3rem; font-weight: 900; color: white; margin: 0 0 15px 0; text-transform: uppercase; line-height: 1.2;}
    .hero-desc { font-size: 1.1rem; color: #EEE; margin-bottom: 25px; }
    
    /* Nút bấm Đỏ (Red Primary Button) */
    .stButton > button[kind="primary"] {
        background-color: #E71A0F; color: white !important; 
        font-weight: 800; border: none; transition: all 0.2s; padding: 10px 0; border-radius: 6px;
    }
    .stButton > button[kind="primary"]:hover { background-color: #C5160D; transform: translateY(-2px); box-shadow: 0 4px 10px rgba(231, 26, 15, 0.3); }

    /* THẺ PHIM (MOVIE CARD) CHUẨN CGV */
    .movie-card {
        background: transparent;
        overflow: hidden; transition: transform 0.3s; height: 100%; margin-bottom: 5px;
    }
    .img-wrapper { 
        width: 100%; aspect-ratio: 2 / 3; position: relative; 
        border-radius: 8px; overflow: hidden; border: 1px solid #EBEBEB;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.5s; }
    .img-wrapper:hover img { transform: scale(1.05); }
    
    /* Nhãn dán độ tuổi (Age Badge) góc trái ảnh */
    .age-badge {
        position: absolute; top: 10px; left: 10px; padding: 4px 8px;
        font-size: 0.9rem; font-weight: 900; color: white;
        border-radius: 4px; border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3); z-index: 10;
    }
    .bg-P { background-color: #4CAF50; } /* Màu xanh lá */
    .bg-K { background-color: #2196F3; } /* Màu xanh dương */
    .bg-T13 { background-color: #FFC107; color: #111; } /* Màu vàng */
    .bg-T16 { background-color: #FF9800; } /* Màu cam */
    .bg-T18 { background-color: #E71A0F; } /* Màu đỏ */

    /* Thông tin phim */
    .movie-info { padding: 15px 0; }
    .movie-title { 
        font-size: 1.1rem; font-weight: 800; color: #222; margin: 0 0 10px 0; 
        text-transform: uppercase; line-height: 1.3;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8rem;
    }
    .movie-meta { font-size: 0.9rem; color: #555; margin: 0 0 5px 0; line-height: 1.5; }
    .movie-meta b { color: #333; }
    
    /* Màn hình chiếu phim */
    .seat-screen { background: #E71A0F; text-align: center; color: white; font-weight: 900; padding: 5px; border-radius: 4px; margin-bottom: 30px; letter-spacing: 5px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR: ĐĂNG NHẬP / ĐĂNG KÝ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #E71A0F;'>🔒 TÀI KHOẢN</h2>", unsafe_allow_html=True)
    
    if not st.session_state.is_logged_in:
        st.info("Vui lòng đăng nhập hệ thống.")
        
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
            st.session_state.selected_seats = []
            st.rerun()

# ==========================================
# 6. KHUNG GIAO DIỆN CHÍNH
# ==========================================
st.markdown("""
<div class="nav-container">
    <div class="nav-logo">SUNNYX<span>CINEMA</span></div>
    <div style="color: #333; font-weight: bold; font-size: 0.9rem;">📍 CƠ SỞ DUY NHẤT: SUNNYX CENTER</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# A. GIAO DIỆN QUẢN TRỊ VIÊN (ADMIN DASHBOARD)
# ------------------------------------------
if st.session_state.user_role == 'admin':
    st.markdown("<h2 style='color:#E71A0F;'>⚙️ BẢNG ĐIỀU KHIỂN QUẢN TRỊ</h2>", unsafe_allow_html=True)
    
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
                st.selectbox("Độ tuổi", ["P", "K", "T13", "T16", "T18"])
                if st.form_submit_button("LƯU PHIM", type="primary"):
                    st.success("Lưu vào movies.csv thành công!")

    with tab_showtimes:
        st.subheader("Quản lý Suất Chiếu")
        st.write("Sắp xếp lịch chiếu phim.")

    with tab_rooms:
        st.subheader("Danh sách Phòng chiếu")
        st.write("Quản lý tình trạng phòng.")

# ------------------------------------------
# B. GIAO DIỆN KHÁCH HÀNG - TRANG CHỦ
# ------------------------------------------
elif st.session_state.current_page == 'home':
    # Banner
    st.markdown("""
    <div class="hero-container">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-tag">ĐỘC QUYỀN TẠI SUNNYX</div>
            <div class="hero-title">DUNE: HÀNH TINH CÁT 2</div>
            <div class="hero-desc">Trải nghiệm âm thanh và hình ảnh sống động nhất tại cơ sở Sunnyx duy nhất của chúng tôi.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Đặt vé nhanh
    with st.container():
        st.markdown('<div class="glass-effect" style="padding: 25px; margin-top: -30px; margin-bottom:40px; position:relative; z-index:10;">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#E71A0F; margin-top:0;'>🎟️ MUA VÉ NHANH</h4>", unsafe_allow_html=True)
        
        qb1, qb2, qb3, qb4 = st.columns([2, 1, 1, 1])
        with qb1: st.selectbox("Chọn Phim", ["Dune: Hành Tinh Cát 2", "Doraemon: Nobita và Lâu Đài...", "Star Wars: Mandalorian"])
        with qb2: st.selectbox("Ngày Xem", ["Hôm nay", "Ngày mai"])
        with qb3: st.selectbox("Suất Chiếu", ["09:30 (IMAX)", "13:15 (3D)", "20:30 (2D)"])
        with qb4: 
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("MUA VÉ", type="primary", use_container_width=True):
                if not st.session_state.is_logged_in:
                    st.error("⚠️ Vui lòng đăng nhập để đặt vé!")
                else:
                    navigate_to("booking", "Dune: Hành Tinh Cát 2")
        st.markdown('</div>', unsafe_allow_html=True)

    # Tiêu đề Danh sách phim
    st.markdown("<h2 style='text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 30px;'>PHIM ĐANG CHIẾU</h2>", unsafe_allow_html=True)
    cols = st.columns(4)
    
    def create_premium_movie_card(col, title, genre, duration, age, date, img_url):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <div class="img-wrapper">
                    <div class="age-badge bg-{age}">{age}</div>
                    <img src="{img_url}">
                </div>
                <div class="movie-info">
                    <p class="movie-title">{title}</p>
                    <p class="movie-meta"><b>Thể loại:</b> {genre}</p>
                    <p class="movie-meta"><b>Thời lượng:</b> {duration}</p>
                    <p class="movie-meta"><b>Khởi chiếu:</b> {date}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🎟️ MUA VÉ", key=f"btn_{title}", use_container_width=True, type="primary"):
                if not st.session_state.is_logged_in:
                    st.error(f"⚠️ Vui lòng đăng nhập để đặt vé phim {title}!")
                else:
                    navigate_to("booking", title)

    # Khởi tạo các thẻ phim với nhãn độ tuổi (P, K, T13, T16, T18)
    create_premium_movie_card(cols[0], "Phim Điện Ảnh Doraemon: Nobita và Lâu Đài...", "Hoạt Hình, Phiêu Lưu", "101 phút", "P", "22-05-2026", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80")
    create_premium_movie_card(cols[1], "Tạm Biệt Gohan", "Gia Đình", "140 phút", "K", "15-05-2026", "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500&q=80")
    create_premium_movie_card(cols[2], "Ngôi Đền Kỳ Quái 5", "Hài, Kinh Dị", "118 phút", "T16", "29-05-2026", "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=500&q=80")
    create_premium_movie_card(cols[3], "Star Wars: Mandalorian và Grogu", "Hành Động, Phiêu Lưu", "132 phút", "T13", "22-05-2026", "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&q=80")

# ------------------------------------------
# C. GIAO DIỆN KHÁCH HÀNG - ĐẶT GHẾ (BOOKING)
# ------------------------------------------
elif st.session_state.current_page == 'booking':
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"): navigate_to("home")
    
    st.markdown(f"## 🎫 ĐẶT VÉ: {st.session_state.selected_movie}")
    st.info("📍 Địa điểm: Sunnyx Cinema Center | 🎬 Phòng: IMAX 01 | ⏰ Suất: 20:30 - Hôm nay")
    
    st.markdown('<div class="seat-screen">MÀN HÌNH</div>', unsafe_allow_html=True)
    st.write("")
    
    # --- GIAO DIỆN CHỌN GHẾ HOÀN TOÀN MỚI BẰNG NÚT BẤM ĐỒNG BỘ ---
    seat_rows = ['A', 'B', 'C', 'D']
    
    for row in seat_rows:
        cols = st.columns(8) # Chia đều 8 cột ngang bằng nhau
        for i, col in enumerate(cols):
            seat_name = f"{row}{i+1}"
            with col:
                # Mô phỏng ghế ngẫu nhiên đã bị đặt (khóa lại)
                is_booked = (hash(seat_name) % 5 == 0) 
                
                if is_booked:
                    st.button(seat_name, key=f"seat_{seat_name}", disabled=True, use_container_width=True)
                else:
                    # Kiểm tra xem ghế này người dùng đang chọn hay chưa
                    is_selected = seat_name in st.session_state.selected_seats
                    
                    # Nếu chọn thì nút chuyển thành màu chính (Đỏ), chưa chọn thì màu phụ (Xám)
                    btn_type = "primary" if is_selected else "secondary"
                    
                    # Hiển thị nút ghế đồng bộ kích thước
                    if st.button(seat_name, key=f"seat_{seat_name}", type=btn_type, use_container_width=True):
                        # Logic bấm nút để Chọn/Hủy ghế
                        if is_selected:
                            st.session_state.selected_seats.remove(seat_name)
                        else:
                            st.session_state.selected_seats.append(seat_name)
                        st.rerun() # Tải lại trang ngay lập tức để đổi màu nút
                        
    st.divider()
    
    num_selected = len(st.session_state.selected_seats)
    col_sum1, col_sum2 = st.columns([3, 1])
    with col_sum1:
        st.markdown(f"**Ghế bạn đang chọn:** {', '.join(st.session_state.selected_seats) if num_selected > 0 else 'Chưa chọn ghế'}")
        st.markdown(f"**Tổng tiền:** <span style='color:#E71A0F; font-size: 1.2rem; font-weight:bold;'>{num_selected * 85000:,} VNĐ</span>", unsafe_allow_html=True)
    with col_sum2:
        if st.button("THANH TOÁN", type="primary", use_container_width=True, disabled=(num_selected==0)):
            st.success("Thanh toán thành công! Vé đã được lưu vào Lịch sử.")
            st.session_state.selected_seats = [] # Reset ghế sau khi mua xong

# ------------------------------------------
# D. GIAO DIỆN KHÁCH HÀNG - LỊCH SỬ VÉ
# ------------------------------------------
elif st.session_state.current_page == 'history':
    if st.button("⬅️ QUAY LẠI TRANG CHỦ"): navigate_to("home")
    
    st.markdown("## 🎫 LỊCH SỬ ĐẶT VÉ CỦA TÔI")
    
    df_history = pd.DataFrame({
        "Mã Vé": ["TK0912", "TK0844"],
        "Tên Phim": ["Star Wars: Mandalorian", "Doraemon: Nobita..."],
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