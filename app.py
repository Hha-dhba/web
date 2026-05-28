import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Sunnyx Vintage Cinema | Classic & Modern",
    page_icon="🎞️",
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
if 'current_page' not in st.session_state: st.session_state.current_page = 'home'
if 'selected_movie' not in st.session_state: st.session_state.selected_movie = ''

if 'selected_seats' not in st.session_state: st.session_state.selected_seats = []
if 'registered_users' not in st.session_state: st.session_state.registered_users = {'admin': '123'}

# ==========================================
# 3. HÀM CHUYỂN TRANG & POPUP QUẢNG CÁO
# ==========================================
def navigate_to(page, movie=""):
    st.session_state.current_page = page
    if movie: 
        st.session_state.selected_movie = movie
        st.session_state.selected_seats = [] 
    st.rerun()

@st.dialog("🎭 SIÊU PHẨM MÙA HÈ TẠI SUNNYX", width="large")
def show_advertisement():
    st.markdown("<h3 style='text-align: center; color: #73171F; margin-top:0; font-family: \"Playfair Display\", serif;'>BOM TẤN ĐÃ ĐỔ BỘ</h3>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070", use_column_width=True)
    st.markdown("<p style='text-align:center; color:#555; margin-top: 15px; font-style: italic;'>Mua vé liền tay, nhận ngay bắp nước miễn phí!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✖ ĐÓNG QUẢNG CÁO", type="primary", use_container_width=True):
            st.session_state.ad_closed = True
            st.rerun()

# ==========================================
# 4. CSS DÀNH CHO GIAO DIỆN (VINTAGE / STEAMPUNK STYLE)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Courier+Prime:wght@400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Courier Prime', monospace; /* Font chữ máy đánh chữ cho nội dung */
    }
    
    h1, h2, h3, h4, h5, h6, .marquee-text, .hero-title, .movie-title {
        font-family: 'Playfair Display', serif !important; /* Font nghệ thuật cho Tiêu đề */
    }

    /* Nền trang màu Kem (Cream) Vintage */
    .stApp { background-color: #F4EFE6; color: #3A2E2A; }
    
    /* Làm nổi bật nút mở Sidebar của Streamlit */
    header { background: transparent !important; }
    button[title="View sidebar"] {
        background-color: #5C161B !important; /* Đỏ đô */
        color: #D4AF37 !important; /* Vàng đồng */
        border: 2px solid #D4AF37 !important;
        border-radius: 5px !important;
        top: 15px; left: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    button[title="View sidebar"] svg { fill: #D4AF37 !important; }

    /* ==========================================
       HIỆU ỨNG TRANG TRÍ (BÁNH RĂNG / GEARS) 
       ========================================== */
    .bg-decoration {
        position: fixed;
        z-index: 0;
        opacity: 0.05; /* Rất mờ để không làm rối mắt */
        pointer-events: none;
        animation: spin 30s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    .gear-1 { top: -50px; left: -50px; font-size: 250px; color: #5C161B; }
    .gear-2 { bottom: -80px; right: -50px; font-size: 300px; color: #D4AF37; }
    .gear-3 { top: 40%; left: -80px; font-size: 150px; color: #3A2E2A; animation: spin 20s linear infinite reverse;}

    /* BẢNG HIỆU ĐÈN MARQUEE (NAVBAR) */
    .vintage-marquee {
        background-color: #2A080A; /* Đen pha đỏ cực đậm */
        border: 4px dotted #D4AF37; /* Viền bóng đèn vàng */
        padding: 20px 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(92, 22, 27, 0.4), inset 0 0 20px rgba(0,0,0,0.8);
        border-radius: 8px;
        position: relative;
        z-index: 10;
    }
    .marquee-text {
        font-size: 3rem; font-weight: 900; margin: 0; letter-spacing: 6px;
        color: #FFF2C8;
        text-shadow: 0 0 5px #D4AF37, 0 0 15px #D4AF37, 0 0 30px #E7A310; /* Hiệu ứng phát sáng neon */
        text-transform: uppercase;
    }
    .marquee-sub { color: #D4AF37; font-size: 1rem; letter-spacing: 3px; border-top: 1px solid #D4AF37; padding-top: 5px; margin-top: 5px; display: inline-block;}

    /* KHUNG VÉ GIẤY (QUICK BOOKING & MOVIE CARDS) */
    .vintage-ticket {
        background-color: #FDFBF7;
        border: 2px dashed #B89947; /* Viền đứt nét giả lập vé giấy xé */
        padding: 25px;
        border-radius: 12px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.08);
        position: relative;
        margin-bottom: 20px;
        z-index: 10;
    }
    /* Khoét lỗ tròn 2 bên để giống hình cái vé thật */
    .vintage-ticket::before, .vintage-ticket::after {
        content: ''; position: absolute; top: 50%; transform: translateY(-50%);
        width: 30px; height: 30px; background-color: #F4EFE6; border-radius: 50%;
        border: 2px dashed #B89947;
    }
    .vintage-ticket::before { left: -16px; border-left-color: transparent; border-top-color: transparent; border-bottom-color: transparent; transform: translateY(-50%) rotate(45deg);}
    .vintage-ticket::after { right: -16px; border-right-color: transparent; border-top-color: transparent; border-bottom-color: transparent; transform: translateY(-50%) rotate(-45deg);}

    .ticket-title { color: #5C161B; font-weight: 900; font-size: 1.5rem; text-transform: uppercase; text-align: center; border-bottom: 2px solid #5C161B; padding-bottom: 10px; margin-bottom: 20px;}

    /* CHỈNH LẠI SELECTBOX & NÚT BẤM VINTAGE */
    .stSelectbox > div > div { background-color: #F4EFE6 !important; border: 1px solid #B89947 !important; border-radius: 4px; color: #3A2E2A !important; font-family: 'Courier Prime', monospace;}
    
    .stButton > button[kind="primary"] {
        background-color: #5C161B; color: #D4AF37 !important; 
        font-family: 'Playfair Display', serif; font-weight: 800; font-size: 1.1rem; letter-spacing: 1px;
        border: 2px solid #D4AF37; transition: all 0.3s; padding: 10px 0; border-radius: 4px;
        box-shadow: 2px 2px 0px #D4AF37; /* Đổ bóng cứng phong cách retro */
    }
    .stButton > button[kind="primary"]:hover { background-color: #731C22; transform: translate(2px, 2px); box-shadow: 0px 0px 0px #D4AF37; }

    .stButton > button[kind="secondary"] {
        background-color: #E8DCC4; color: #5C161B !important; 
        font-family: 'Playfair Display', serif; font-weight: 700;
        border: 1px solid #B89947; transition: all 0.2s; border-radius: 4px;
    }
    .stButton > button[kind="secondary"]:hover { background-color: #D4AF37; color: white !important;}

    /* THẺ PHIM (DÙNG NỀN TRẮNG KEM, GIỮ NGUYÊN MÀU POSTER) */
    .movie-card-container > div > div > div[data-testid="stVerticalBlock"] {
        background: #FDFBF7 !important; padding: 0 !important; border-radius: 8px;
        border: 1px solid #D4AF37; box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s; height: 100%; margin-bottom: 10px; z-index: 10; position: relative;
    }
    .movie-card-container > div > div > div[data-testid="stVerticalBlock"]:hover { transform: translateY(-5px); box-shadow: 5px 5px 15px rgba(92,22,27,0.3); border-color: #5C161B;}
    
    .img-wrapper { 
        width: 100%; aspect-ratio: 2 / 3; overflow: hidden;
        border-bottom: 2px solid #D4AF37; padding: 5px; background: #FFF;
    }
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.5s; border-radius: 4px;}
    .movie-card-container > div > div > div[data-testid="stVerticalBlock"]:hover .img-wrapper img { transform: scale(1.05); }
    
    .content-container { padding: 15px; text-align: center; }
    .movie-title { font-size: 1.1rem !important; font-weight: 900 !important; color: #5C161B !important; text-transform: uppercase; margin-bottom: 10px !important; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8rem;}
    .movie-info-text { font-size: 0.85rem; color: #555; margin: 0 0 5px 0; border-bottom: 1px dotted #CCC; padding-bottom: 5px;}

    /* GIAO DIỆN CHỌN GHẾ - GHẾ NHUNG CỔ ĐIỂN */
    .seat-screen { background: #5C161B; text-align: center; color: #D4AF37; font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 900; padding: 10px; border-radius: 4px; margin-bottom: 30px; letter-spacing: 8px; border: 2px double #D4AF37; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);}
    
    /* Ẩn bớt các khoảng trắng thừa của Streamlit */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid #5C161B; }
    .stTabs [data-baseweb="tab"] { color: #555; font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.2rem; }
    .stTabs [aria-selected="true"] { color: #5C161B !important; border-bottom: 3px solid #5C161B !important; }
</style>
""", unsafe_allow_html=True)

# Các bánh răng trang trí xoay dưới nền
st.markdown("""
<div class="bg-decoration gear-1">⚙</div>
<div class="bg-decoration gear-2">⚙</div>
<div class="bg-decoration gear-3">⚙</div>
""", unsafe_allow_html=True)


# ==========================================
# 5. SIDEBAR: ĐĂNG NHẬP (Phong cách Vintage)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #5C161B; font-family: \"Playfair Display\", serif;'>🗝️ PHÒNG VÉ</h2>", unsafe_allow_html=True)
    
    if not st.session_state.is_logged_in:
        st.info("Vui lòng xuất trình thẻ thành viên (Đăng nhập).")
        
        tab_login, tab_register = st.tabs(["🔑 Vào Cửa", "📝 Đăng Ký"])
        
        with tab_login:
            with st.form("login_form"):
                st.markdown("<small>*(Gợi ý: Tài khoản `admin` - Pass `123`)*</small>", unsafe_allow_html=True)
                username_input = st.text_input("Bí danh (Username)")
                password_input = st.text_input("Mật mã (Password)", type="password")
                submitted = st.form_submit_button("XÁC NHẬN", type="primary")
                
                if submitted:
                    if username_input == "" or password_input == "": st.error("Thiếu thông tin!")
                    elif username_input in st.session_state.registered_users and st.session_state.registered_users[username_input] == password_input:
                        st.session_state.is_logged_in = True
                        st.session_state.username = username_input
                        st.session_state.user_role = "admin" if username_input.lower() == 'admin' else "customer"
                        st.session_state.current_page = "admin_dash" if username_input.lower() == 'admin' else "home"
                        st.rerun()
                    else:
                        if password_input == "123" and username_input != 'admin':
                            st.session_state.is_logged_in = True
                            st.session_state.username = username_input
                            st.session_state.user_role = "customer"
                            st.session_state.current_page = "home"
                            st.rerun()
                        else:
                            st.error("Thông tin không chính xác!")
        
        with tab_register:
            with st.form("register_form"):
                new_username = st.text_input("Bí danh mới")
                new_password = st.text_input("Mật mã", type="password")
                confirm_password = st.text_input("Xác nhận mật mã", type="password")
                reg_submitted = st.form_submit_button("LÀM THẺ", type="primary")
                
                if reg_submitted:
                    if new_username == "" or new_password == "": st.error("Thiếu thông tin!")
                    elif new_password != confirm_password: st.error("Mật mã không khớp!")
                    else:
                        st.session_state.registered_users[new_username] = new_password
                        st.success("Làm thẻ thành công! Sang tab Vào Cửa để tiếp tục.")
                        
    else:
        st.success(f"Kính chào, ngài/quý bà **{st.session_state.username}**.")
        st.caption(f"Hạng: {st.session_state.user_role.upper()}")
        
        if st.session_state.user_role == 'customer':
            if st.button("🏠 Sảnh Chính", use_container_width=True): navigate_to("home")
            if st.button("🎫 Cuống Vé Của Tôi", use_container_width=True): navigate_to("history")
            st.divider()
            
        if st.button("RỜI ĐI (ĐĂNG XUẤT)", use_container_width=True):
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
<div class="vintage-marquee">
    <div class="marquee-text">SUNNYX CINEMA</div>
    <div class="marquee-sub">EST. 1926 • THE GRAND THEATER</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# A. GIAO DIỆN QUẢN TRỊ VIÊN (ADMIN DASHBOARD)
# ------------------------------------------
if st.session_state.user_role == 'admin':
    st.markdown("<h2 style='color:#5C161B;'>⚙️ PHÒNG ĐIỀU HÀNH KỸ THUẬT</h2>", unsafe_allow_html=True)
    st.info("Khu vực dành riêng cho Quản đốc rạp (Admin).")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Doanh thu", "45.000.000 đ", "+15%")
    c2.metric("Vé xuất ra", "320 vé", "+24")
    c3.metric("Phim trình chiếu", "8 cuộn", "0")
    c4.metric("Thành viên mới", "45", "+5")
    
    st.divider()
    tab_movies, tab_showtimes, tab_rooms = st.tabs(["🎞️ Kho Phim", "🕰️ Lịch Chiếu", "🪑 Phòng Chiếu"])
    
    with tab_movies:
        st.write("Bảng điều khiển lưu trữ các cuộn phim hiện đại.")

# ------------------------------------------
# B. GIAO DIỆN KHÁCH HÀNG - TRANG CHỦ
# ------------------------------------------
elif st.session_state.current_page == 'home':
    
    # Khung Đặt vé nhanh (Thiết kế như Vé giấy xé rãnh)
    with st.container():
        st.markdown('<div class="vintage-ticket">', unsafe_allow_html=True)
        st.markdown('<div class="ticket-title">🎟️ QUẦY BÁN VÉ NHANH</div>', unsafe_allow_html=True)
        
        qb1, qb2, qb3, qb4 = st.columns([2, 1, 1, 1])
        with qb1: st.selectbox("Chọn Cuộn Phim", ["Dune: Hành Tinh Cát 2", "Doraemon: Nobita và Lâu Đài...", "Star Wars: Mandalorian"])
        with qb2: st.selectbox("Ngày Chiếu", ["Hôm nay", "Ngày mai"])
        with qb3: st.selectbox("Khung Giờ", ["09:30 (IMAX)", "13:15 (3D)", "20:30 (2D)"])
        with qb4: 
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("XUẤT VÉ", type="primary", use_container_width=True):
                if not st.session_state.is_logged_in:
                    st.error("⚠️ Quý khách vui lòng xuất trình thẻ thành viên (Đăng nhập góc trái)!")
                else:
                    navigate_to("booking", "Dune: Hành Tinh Cát 2")
        st.markdown('</div>', unsafe_allow_html=True)

    # Tiêu đề Danh sách phim
    st.markdown("<h2 style='text-align: center; color: #5C161B; margin-top: 40px; margin-bottom: 30px; position:relative; z-index:10;'>— CÁC TÁC PHẨM TRÌNH CHIẾU —</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="movie-card-container">', unsafe_allow_html=True)
    cols = st.columns(4)
    
    def create_premium_movie_card(col, title, genre, duration, rating, img_url):
        with col:
            with st.container():
                st.markdown(f"""
                <div class="img-wrapper"><img src="{img_url}"></div>
                <div class="content-container">
                    <p class="movie-title">{title}</p>
                    <p class="movie-info-text"><b>Thể loại:</b> {genre}</p>
                    <p class="movie-info-text"><b>Độ dài:</b> {duration}</p>
                    <p class="movie-info-text" style="color: #D4AF37; font-weight: bold;">Đánh giá: ⭐ {rating}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🎟️ MUA VÉ", key=f"btn_{title}", use_container_width=True, type="primary"):
                    if not st.session_state.is_logged_in:
                        st.error(f"⚠️ Vui lòng đăng nhập để đặt vé!")
                    else:
                        navigate_to("booking", title)

    # Poster cập nhật theo thời đại, giữ nguyên màu gốc
    create_premium_movie_card(cols[0], "Phim Điện Ảnh Doraemon: Lâu Đài Dưới Đáy Biển", "Hoạt Hình", "101 phút", "9.2", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80")
    create_premium_movie_card(cols[1], "Dune: Hành Tinh Cát 2", "Viễn Tưởng", "166 phút", "9.5", "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&q=80")
    create_premium_movie_card(cols[2], "Ngôi Đền Kỳ Quái 5", "Hài, Kinh Dị", "118 phút", "8.5", "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=500&q=80")
    create_premium_movie_card(cols[3], "Godzilla x Kong: Đế Chế Mới", "Hành Động", "115 phút", "9.0", "https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=500&q=80")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# C. GIAO DIỆN KHÁCH HÀNG - ĐẶT GHẾ (BOOKING)
# ------------------------------------------
elif st.session_state.current_page == 'booking':
    if st.button("⬅️ TRỞ VỀ SẢNH CHÍNH", type="secondary"): navigate_to("home")
    
    st.markdown(f"<h2 style='color:#5C161B;'>🎫 XUẤT VÉ: {st.session_state.selected_movie}</h2>", unsafe_allow_html=True)
    st.info("📍 Địa điểm: The Grand Theater Sunnyx | 🎬 Phòng Hát số 1 | ⏰ 20:30")
    
    st.markdown('<div class="seat-screen">MÀN CHIẾU BẠC</div>', unsafe_allow_html=True)
    st.write("")
    
    # Sơ đồ ghế 
    seat_rows = ['A', 'B', 'C', 'D']
    for row in seat_rows:
        cols = st.columns(8)
        for i, col in enumerate(cols):
            seat_name = f"{row}{i+1}"
            with col:
                is_booked = (hash(seat_name) % 5 == 0) 
                if is_booked:
                    st.button(seat_name, key=f"seat_{seat_name}", disabled=True, use_container_width=True)
                else:
                    is_selected = seat_name in st.session_state.selected_seats
                    btn_type = "primary" if is_selected else "secondary"
                    
                    if st.button(seat_name, key=f"seat_{seat_name}", type=btn_type, use_container_width=True):
                        if is_selected: st.session_state.selected_seats.remove(seat_name)
                        else: st.session_state.selected_seats.append(seat_name)
                        st.rerun() 
                        
    st.divider()
    
    num_selected = len(st.session_state.selected_seats)
    col_sum1, col_sum2 = st.columns([3, 1])
    with col_sum1:
        st.markdown(f"**Vị trí đã chọn:** {', '.join(st.session_state.selected_seats) if num_selected > 0 else 'Chưa chọn'}")
        st.markdown(f"**Lệ phí:** <span style='color:#5C161B; font-size: 1.2rem; font-weight:bold;'>{num_selected * 85000:,} VNĐ</span>", unsafe_allow_html=True)
    with col_sum2:
        if st.button("TRẢ TIỀN & NHẬN VÉ", type="primary", use_container_width=True, disabled=(num_selected==0)):
            st.success("Giao dịch thành công! Xin kính chúc quý khách xem phim vui vẻ.")
            st.session_state.selected_seats = [] 

# ------------------------------------------
# D. GIAO DIỆN KHÁCH HÀNG - LỊCH SỬ VÉ
# ------------------------------------------
elif st.session_state.current_page == 'history':
    if st.button("⬅️ TRỞ VỀ SẢNH CHÍNH", type="secondary"): navigate_to("home")
    
    st.markdown("<h2 style='color:#5C161B;'>🎫 BỘ SƯU TẬP CUỐNG VÉ</h2>", unsafe_allow_html=True)
    
    df_history = pd.DataFrame({
        "Mã Vé": ["TK0912", "TK0844"],
        "Tên Phim": ["Star Wars: Mandalorian", "Doraemon: Nobita..."],
        "Ghế": ["C4, C5", "F10"],
        "Ngày Chiếu": ["20/05/2026", "15/05/2026"],
        "Lệ phí": ["170.000 đ", "95.000 đ"],
        "Trạng thái": ["Đã xem", "Đã xem"]
    })
    st.dataframe(df_history, use_container_width=True, hide_index=True)

# ==========================================
# 7. GỌI HIỂN THỊ QUẢNG CÁO TẠI TRANG CHỦ
# ==========================================
if not st.session_state.ad_closed and st.session_state.current_page == 'home' and st.session_state.user_role != 'admin':
    show_advertisement()