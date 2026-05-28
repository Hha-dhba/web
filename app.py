import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components # Thêm thư viện để nhúng HTML/JS

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
        font-family: 'Courier Prime', monospace; 
    }
    
    h1, h2, h3, h4, h5, h6, .marquee-text, .hero-title, .movie-title {
        font-family: 'Playfair Display', serif !important; 
    }

    /* Nền trang màu Kem (Cream) Vintage */
    .stApp { background-color: #F4EFE6; color: #3A2E2A; }
    
    /* Làm nổi bật nút mở Sidebar */
    header { background: transparent !important; }
    button[title="View sidebar"] {
        background-color: #5C161B !important; color: #D4AF37 !important; border: 2px solid #D4AF37 !important;
        border-radius: 5px !important; top: 15px; left: 15px; box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    button[title="View sidebar"] svg { fill: #D4AF37 !important; }

    /* Hiệu ứng trang trí bánh răng */
    .bg-decoration { position: fixed; z-index: 0; opacity: 0.05; pointer-events: none; animation: spin 30s linear infinite; }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    .gear-1 { top: -50px; left: -50px; font-size: 250px; color: #5C161B; }
    .gear-2 { bottom: -80px; right: -50px; font-size: 300px; color: #D4AF37; }
    .gear-3 { top: 40%; left: -80px; font-size: 150px; color: #3A2E2A; animation: spin 20s linear infinite reverse;}

    /* Bảng hiệu Navbar */
    .vintage-marquee {
        background-color: #2A080A; border: 4px dotted #D4AF37; padding: 20px 30px; text-align: center;
        margin-bottom: 30px; box-shadow: 0 10px 20px rgba(92, 22, 27, 0.4), inset 0 0 20px rgba(0,0,0,0.8);
        border-radius: 8px; position: relative; z-index: 10;
    }
    .marquee-text {
        font-size: 3rem; font-weight: 900; margin: 0; letter-spacing: 6px; color: #FFF2C8;
        text-shadow: 0 0 5px #D4AF37, 0 0 15px #D4AF37, 0 0 30px #E7A310; text-transform: uppercase;
    }
    .marquee-sub { color: #D4AF37; font-size: 1rem; letter-spacing: 3px; border-top: 1px solid #D4AF37; padding-top: 5px; margin-top: 5px; display: inline-block;}

    /* Khung Vé Giấy (Quick Booking) */
    .vintage-ticket {
        background-color: #FDFBF7; border: 2px dashed #B89947; padding: 25px; border-radius: 12px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.08); position: relative; margin-bottom: 30px; z-index: 10;
    }
    .vintage-ticket::before, .vintage-ticket::after {
        content: ''; position: absolute; top: 50%; transform: translateY(-50%); width: 30px; height: 30px; 
        background-color: #F4EFE6; border-radius: 50%; border: 2px dashed #B89947;
    }
    .vintage-ticket::before { left: -16px; border-left-color: transparent; border-top-color: transparent; border-bottom-color: transparent; transform: translateY(-50%) rotate(45deg);}
    .vintage-ticket::after { right: -16px; border-right-color: transparent; border-top-color: transparent; border-bottom-color: transparent; transform: translateY(-50%) rotate(-45deg);}
    .ticket-title { color: #5C161B; font-weight: 900; font-size: 1.5rem; text-transform: uppercase; text-align: center; border-bottom: 2px solid #5C161B; padding-bottom: 10px; margin-bottom: 20px;}

    /* Form UI */
    .stSelectbox > div > div { background-color: #F4EFE6 !important; border: 1px solid #B89947 !important; border-radius: 4px; color: #3A2E2A !important; font-family: 'Courier Prime', monospace;}
    
    .stButton > button[kind="primary"] {
        background-color: #5C161B; color: #D4AF37 !important; font-family: 'Playfair Display', serif; 
        font-weight: 800; font-size: 1.1rem; letter-spacing: 1px; border: 2px solid #D4AF37; 
        transition: all 0.3s; padding: 10px 0; border-radius: 4px; box-shadow: 2px 2px 0px #D4AF37; 
    }
    .stButton > button[kind="primary"]:hover { background-color: #731C22; transform: translate(2px, 2px); box-shadow: 0px 0px 0px #D4AF37; }

    .stButton > button[kind="secondary"] {
        background-color: #E8DCC4; color: #5C161B !important; font-family: 'Playfair Display', serif; 
        font-weight: 700; border: 1px solid #B89947; transition: all 0.2s; border-radius: 4px;
    }
    .stButton > button[kind="secondary"]:hover { background-color: #D4AF37; color: white !important;}

    /* Thẻ Phim (Movie Cards) */
    .movie-card-container > div > div > div[data-testid="stVerticalBlock"] {
        background: #FDFBF7 !important; padding: 0 !important; border-radius: 8px; border: 1px solid #D4AF37; 
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1); transition: transform 0.3s; height: 100%; margin-bottom: 20px; z-index: 10; position: relative;
    }
    .movie-card-container > div > div > div[data-testid="stVerticalBlock"]:hover { transform: translateY(-5px); box-shadow: 5px 5px 15px rgba(92,22,27,0.3); border-color: #5C161B;}
    
    .img-wrapper { width: 100%; aspect-ratio: 2 / 3; overflow: hidden; border-bottom: 2px solid #D4AF37; padding: 5px; background: #FFF;}
    .img-wrapper img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.5s; border-radius: 4px;}
    .movie-card-container > div > div > div[data-testid="stVerticalBlock"]:hover .img-wrapper img { transform: scale(1.05); }
    
    .content-container { padding: 15px; text-align: center; }
    .movie-title { font-size: 1.1rem !important; font-weight: 900 !important; color: #5C161B !important; text-transform: uppercase; margin-bottom: 10px !important; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8rem;}
    .movie-info-text { font-size: 0.85rem; color: #555; margin: 0 0 5px 0; border-bottom: 1px dotted #CCC; padding-bottom: 5px;}

    /* Ghế ngồi */
    .seat-screen { background: #5C161B; text-align: center; color: #D4AF37; font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 900; padding: 10px; border-radius: 4px; margin-bottom: 30px; letter-spacing: 8px; border: 2px double #D4AF37; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);}
</style>
""", unsafe_allow_html=True)

# Trang trí
st.markdown("""
<div class="bg-decoration gear-1">⚙</div>
<div class="bg-decoration gear-2">⚙</div>
<div class="bg-decoration gear-3">⚙</div>
""", unsafe_allow_html=True)


# ==========================================
# 5. SIDEBAR: ĐĂNG NHẬP
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
    <div class="marquee-sub">EST. 1926 • CLASSIC VINTAGE CINEMA</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# A. GIAO DIỆN QUẢN TRỊ VIÊN
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
    tab_movies, tab_showtimes = st.tabs(["🎞️ Kho Phim", "🕰️ Lịch Chiếu"])
    with tab_movies: st.write("Bảng điều khiển lưu trữ các cuộn phim hiện đại.")

# ------------------------------------------
# B. GIAO DIỆN KHÁCH HÀNG - TRANG CHỦ
# ------------------------------------------
elif st.session_state.current_page == 'home':

    # --- TÍNH NĂNG MỚI: SLIDER CAROUSEL PHIM HOT BẰNG HTML/JS ---
    st.markdown("<h2 style='text-align: center; color: #5C161B; margin-bottom: 20px; z-index:10; position:relative;'>— TÂM ĐIỂM TUẦN NÀY —</h2>", unsafe_allow_html=True)
    
    # Khối mã HTML/JS tạo Slider
    slider_html = """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Courier+Prime:wght@400;700&display=swap');
      body { margin: 0; background-color: transparent; font-family: 'Playfair Display', serif;}
      .slider-container { width: 100%; height: 350px; position: relative; overflow: hidden; border: 4px double #D4AF37; border-radius: 10px; background: #2A080A; box-shadow: 0 10px 20px rgba(0,0,0,0.3);}
      .slide { position: absolute; width: 100%; height: 100%; display: flex; transition: opacity 1s ease-in-out; opacity: 0; }
      .slide.active { opacity: 1; z-index: 10; }
      .poster { width: 35%; height: 100%; background-size: cover; background-position: center; border-right: 2px dashed #D4AF37; }
      .content { width: 65%; padding: 30px; color: #FFF2C8; display: flex; flex-direction: column; justify-content: center; }
      h1 { color: #D4AF37; font-size: 32px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px; line-height: 1.2;}
      p { font-family: 'Courier Prime', monospace; font-size: 15px; line-height: 1.6; color: #E8DCC4; margin-bottom: 15px;}
      .tag { display: inline-block; border: 1px solid #D4AF37; padding: 5px 12px; font-size: 13px; margin-right: 10px; color: #D4AF37; font-family: 'Courier Prime', monospace;}
      .nav-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: #D4AF37; border: 1px solid #D4AF37; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 20px; font-weight: bold; z-index: 20; transition: 0.3s;}
      .nav-btn:hover { background: #D4AF37; color: #2A080A;}
      .prev { left: 10px; } .next { right: 10px; }
    </style>

    <div class="slider-container">
      <div class="slide active">
        <div class="poster" style="background-image: url('https://images.unsplash.com/photo-1533158307598-773428a39dbd?q=80&w=1000');"></div>
        <div class="content">
          <h1>Furiosa: Câu Chuyện Từ Mad Max</h1>
          <p>Phần tiền truyện hoành tráng đưa khán giả trở lại Wasteland khắc nghiệt. Theo chân nữ chiến binh Furiosa trẻ tuổi trong hành trình sinh tồn và báo thù đẫm máu.</p>
          <div><span class="tag">Hành Động</span><span class="tag">IMAX 2D</span><span class="tag">⭐ 9.2</span></div>
        </div>
      </div>
      <div class="slide">
        <div class="poster" style="background-image: url('https://images.unsplash.com/photo-1616530940355-351fabd9524b?q=80&w=1000');"></div>
        <div class="content">
          <h1>Hành Tinh Cát 2 (Dune: Part Two)</h1>
          <p>Paul Atreides liên minh cùng Chani và người Fremen trên con đường trả thù những kẻ đã hủy hoại gia đình anh. Một kiệt tác thị giác không thể bỏ lỡ.</p>
          <div><span class="tag">Viễn Tưởng</span><span class="tag">IMAX 3D</span><span class="tag">⭐ 9.5</span></div>
        </div>
      </div>
      <div class="slide">
        <div class="poster" style="background-image: url('https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?q=80&w=1000');"></div>
        <div class="content">
          <h1>Lật Mặt 7: Một Điều Ước</h1>
          <p>Tác phẩm điện ảnh lấy đi nước mắt của hàng triệu khán giả Việt. Câu chuyện cảm động về tình mẫu tử, sự hy sinh và những góc khuất trong gia đình.</p>
          <div><span class="tag">Tâm Lý, Gia Đình</span><span class="tag">2D Phụ Đề</span><span class="tag">⭐ 9.0</span></div>
        </div>
      </div>
      
      <button class="nav-btn prev" onclick="moveSlide(-1)">&#10094;</button>
      <button class="nav-btn next" onclick="moveSlide(1)">&#10095;</button>
    </div>

    <script>
      let currentSlide = 0;
      const slides = document.querySelectorAll('.slide');
      let slideInterval;

      function showSlide(index) {
        slides.forEach(s => s.classList.remove('active'));
        if (index >= slides.length) currentSlide = 0;
        else if (index < 0) currentSlide = slides.length - 1;
        else currentSlide = index;
        slides[currentSlide].classList.add('active');
      }

      function moveSlide(step) {
        showSlide(currentSlide + step);
        resetInterval();
      }

      function resetInterval() {
        clearInterval(slideInterval);
        slideInterval = setInterval(() => moveSlide(1), 4000);
      }
      resetInterval(); // Khởi động auto-slide
    </script>
    """
    # Nhúng khối HTML Slider vào Streamlit
    components.html(slider_html, height=360)


    # Đặt vé nhanh
    with st.container():
        st.markdown('<div class="vintage-ticket">', unsafe_allow_html=True)
        st.markdown('<div class="ticket-title">🎟️ QUẦY BÁN VÉ NHANH</div>', unsafe_allow_html=True)
        
        qb1, qb2, qb3, qb4 = st.columns([2, 1, 1, 1])
        with qb1: st.selectbox("Chọn Cuộn Phim", ["Furiosa: Mad Max", "Dune: Hành Tinh Cát 2", "Lật Mặt 7", "Doraemon", "Godzilla x Kong"])
        with qb2: st.selectbox("Ngày Chiếu", ["Hôm nay", "Ngày mai"])
        with qb3: st.selectbox("Khung Giờ", ["09:30 (IMAX)", "13:15 (3D)", "20:30 (2D)"])
        with qb4: 
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("XUẤT VÉ", type="primary", use_container_width=True):
                if not st.session_state.is_logged_in:
                    st.error("⚠️ Xuất trình thẻ thành viên (Đăng nhập)!")
                else:
                    navigate_to("booking", "Furiosa: Mad Max")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TÍNH NĂNG MỚI: NHIỀU PHIM HƠN (2 HÀNG) ---
    st.markdown("<h2 style='text-align: center; color: #5C161B; margin-top: 40px; margin-bottom: 30px; position:relative; z-index:10;'>— CÁC TÁC PHẨM TRÌNH CHIẾU —</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="movie-card-container">', unsafe_allow_html=True)
    
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

    # Hàng 1 (4 Phim)
    r1_cols = st.columns(4)
    create_premium_movie_card(r1_cols[0], "Furiosa: A Mad Max Saga", "Hành Động", "148 phút", "9.2", "https://images.unsplash.com/photo-1533158307598-773428a39dbd?w=500&q=80")
    create_premium_movie_card(r1_cols[1], "Dune: Hành Tinh Cát 2", "Viễn Tưởng", "166 phút", "9.5", "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&q=80")
    create_premium_movie_card(r1_cols[2], "Lật Mặt 7: Một Điều Ước", "Tâm Lý", "138 phút", "9.0", "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=500&q=80")
    create_premium_movie_card(r1_cols[3], "Doraemon: Bản Giao Hưởng", "Hoạt Hình", "115 phút", "8.5", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80")
    
    st.write("") # Khoảng cách giữa 2 hàng
    
    # Hàng 2 (4 Phim Mới)
    r2_cols = st.columns(4)
    create_premium_movie_card(r2_cols[0], "Godzilla x Kong: Đế Chế Mới", "Hành Động", "115 phút", "8.8", "https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=500&q=80")
    create_premium_movie_card(r2_cols[1], "Hành Tinh Khỉ: Vương Quốc Mới", "Viễn Tưởng", "145 phút", "8.7", "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500&q=80")
    create_premium_movie_card(r2_cols[2], "Garfield: Mèo Béo Siêu Quậy", "Hài, Hoạt Hình", "101 phút", "8.2", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500&q=80")
    create_premium_movie_card(r2_cols[3], "Exhuma: Quật Mộ Trùng Ma", "Kinh Dị", "134 phút", "9.1", "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=500&q=80")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# C. GIAO DIỆN KHÁCH HÀNG - ĐẶT GHẾ (BOOKING)
# ------------------------------------------
elif st.session_state.current_page == 'booking':
    if st.button("⬅️ TRỞ VỀ SẢNH CHÍNH", type="secondary"): navigate_to("home")
    
    st.markdown(f"<h2 style='color:#5C161B;'>🎫 XUẤT VÉ: {st.session_state.selected_movie}</h2>", unsafe_allow_html=True)
    st.info("📍 Địa điểm: Sunnyx Vintage Cinema | 🎬 Phòng Chiếu số 1 | ⏰ 20:30")
    
    st.markdown('<div class="seat-screen">MÀN CHIẾU BẠC</div>', unsafe_allow_html=True)
    st.write("")
    
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
# 7. QUẢNG CÁO POPUP
# ==========================================
if not st.session_state.ad_closed and st.session_state.current_page == 'home' and st.session_state.user_role != 'admin':
    show_advertisement()