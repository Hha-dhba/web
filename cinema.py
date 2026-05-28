import streamlit as st

st.set_page_config(
    page_title="Rạp Phim An An ☀️ | Đỉnh Cao Điện Ảnh",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Import font Montserrat hiện đại, mạnh mẽ */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* --- MÀU NỀN HỆ THỐNG (Gradient Hồng Phấn) --- */
    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%); /* LavenderBlush to MistyRose */
        color: #333333;
    }
    
    /* Xóa khoảng trắng thừa và ẩn header */
    .block-container { padding-top: 1rem !important; max-width: 1400px; }
    header {visibility: hidden;}

    /* =========================================
       HIỆU ỨNG GLASSMORPHISM (Kính mờ) CHUNG
    ========================================= */
    .glass-effect {
        background: rgba(255, 255, 255, 0.25); /* Nền trắng trong suốt */
        box-shadow: 0 8px 32px 0 rgba(255, 20, 147, 0.15); /* Bóng đổ hồng nhẹ */
        backdrop-filter: blur(12px); /* Hiệu ứng làm mờ nền sau */
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4); /* Viền kính sáng */
        border-radius: 16px;
    }

    /* --- NAVBAR (Thanh điều hướng) --- */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 30px;
        margin-bottom: 30px;
        /* Áp dụng Glassmorphism */
        background: rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    .nav-logo { font-size: 1.8rem; font-weight: 900; color: #333; margin: 0; }
    .nav-logo span { color: #FF1493; } /* Chữ Cinema màu hồng */
    
    .nav-menu { display: flex; gap: 15px; }
    .nav-button {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(255, 20, 147, 0.3);
        color: #FF1493;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
        text-decoration: none; /* Cho thẻ a nếu dùng */
        display: inline-block;
    }
    .nav-button:hover {
        background: #FF1493;
        color: white;
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.4);
        transform: translateY(-2px);
        border-color: transparent;
    }

    /* --- HERO BANNER KHỔNG LỒ (Nâng cấp) --- */
    .hero-container {
        /* Sử dụng ảnh chất lượng cao, kịch tính hơn */
        background-image: url('https://images.unsplash.com/photo-1533158307598-773428a39dbd?q=80&w=2070');
        background-size: cover;
        background-position: center 30%; /* Căn chỉnh vị trí ảnh */
        height: 500px;
        border-radius: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 60px;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }
    
    /* Lớp phủ gradient để làm nổi bật chữ */
    .hero-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to right, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 60%, rgba(0,0,0,0.1) 100%);
        z-index: 1;
    }
    
    .hero-content {
        position: relative;
        z-index: 2; /* Đặt nội dung lên trên lớp phủ */
        max-width: 600px;
    }
    
    .hero-tag {
        color: #FFD700; /* Màu vàng kim loại nổi bật */
        font-weight: 800; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 15px;
        display: inline-block; padding: 5px 10px; background: rgba(0,0,0,0.5); border-radius: 5px;
    }
    
    .hero-title {
        font-size: 4rem; font-weight: 900; color: white; margin: 0 0 20px 0;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.5); line-height: 1.1;
    }
    
    .hero-desc { font-size: 1.2rem; color: #EEE; margin-bottom: 30px; font-weight: 500; text-shadow: 1px 1px 5px rgba(0,0,0,0.5); }

    /* Nút Xem Trailer trong Banner */
    .hero-button {
        background: linear-gradient(90deg, #FF1493 0%, #FF69B4 100%);
        color: white; padding: 15px 35px; border-radius: 12px; font-weight: 700; font-size: 1.1rem;
        cursor: pointer; transition: all 0.3s; display: inline-block;
        box-shadow: 0 10px 30px rgba(255, 20, 147, 0.5); border: none;
    }
    .hero-button:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 15px 40px rgba(255, 20, 147, 0.7); }

    /* --- WIDGET MUA VÉ NHANH (Nổi bật hơn) --- */
    .quick-book-container {
        @extend .glass-effect; /* Kế thừa hiệu ứng kính */
        padding: 30px;
        margin-bottom: 40px;
        transform: translateY(-60px); /* Kéo lên đè nhẹ vào banner */
        margin-top: -40px;
    }

    .quick-book-title {
        color: #FF1493; font-weight: 800; text-transform: uppercase; margin-bottom: 20px; font-size: 1.6rem;
        display: flex; align-items: center;
    }
    .quick-book-title::before { content: '🎟️'; margin-right: 10px; font-size: 1.8rem; }

    /* --- TÙY CHỈNH SELECTBOX & NÚT TRONG WIDGET --- */
    /* CSS cho Selectbox của Streamlit để trong suốt */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.5) !important; /* Nền trắng trong suốt */
        color: #333 !important;
        border: 1px solid rgba(255, 20, 147, 0.3) !important;
        backdrop-filter: blur(5px);
        border-radius: 8px;
    }
    
    /* Nút Mua Vé Ngay */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF1493 0%, #FF69B4 100%);
        color: white; border: none; border-radius: 8px; padding: 12px 0; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease;
        width: 100%; box-shadow: 0 5px 15px rgba(255, 20, 147, 0.3);
        height: 100%; /* Để nút cao bằng các ô selectbox */
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 25px rgba(255, 20, 147, 0.6);
    }

    /* --- KHUNG CARD PHIM (POSTER) - GLASSMORPHISM --- */
    .movie-card-container {
        /* Áp dụng trực tiếp cho div bao quanh của Streamlit */
        & > div > div > div[data-testid="stVerticalBlock"] {
            @extend .glass-effect; /* Kế thừa hiệu ứng kính */
            padding: 0 !important; /* Xóa padding mặc định để ảnh tràn viền */
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; /* Hiệu ứng nảy */
            overflow: hidden;
            height: 100%; /* Đảm bảo các card bằng nhau */
            display: flex;
            flex-direction: column;
        }

        /* Hiệu ứng hover cho card */
        & > div > div > div[data-testid="stVerticalBlock"]:hover {
            border-color: #FF1493;
            box-shadow: 0 15px 40px rgba(255, 20, 147, 0.3);
            transform: translateY(-10px) scale(1.02);
        }

        /* Container cho ảnh để áp dụng hiệu ứng zoom */
        .image-container {
            overflow: hidden; border-radius: 16px 16px 0 0; flex-shrink: 0;
        }
        .image-container img {
            transition: transform 0.5s ease; width: 100%; display: block;
        }
        & > div > div > div[data-testid="stVerticalBlock"]:hover .image-container img {
            transform: scale(1.1); /* Zoom ảnh khi hover */
        }
        
        /* Phần nội dung text bên dưới */
        .content-container { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;}
    }

    /* Style cho chữ trong Card */
    h3 {
        font-size: 1.3rem !important; font-weight: 800 !important; margin-bottom: 8px !important;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #222 !important;
    }
    
    /* Style cho thông tin phụ (Điểm, thời lượng, thể loại) */
    .movie-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; color: #555; font-weight: 600; }
    .movie-rating { color: #FF1493; display: flex; align-items: center; }
    .movie-rating span { margin-left: 5px; }
    .movie-genre { color: #777; font-size: 0.9rem; margin-bottom: 15px; font-style: italic; }

    /* Nút Đặt Vé trong Card (Style riêng để không bị kính mờ đè) */
    .card-button > button {
        background: linear-gradient(90deg, #FF1493 0%, #FF69B4 100%);
        color: white; border: none; border-radius: 8px; padding: 10px 0; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease; width: 100%;
        box-shadow: 0 4px 10px rgba(255, 20, 147, 0.3);
    }
    .card-button > button:hover {
        transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 20, 147, 0.6); color: white; border: none;
    }

    /* --- TÙY CHỈNH TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px; border-bottom: none; /* Xóa viền dưới mặc định */
        margin-bottom: 20px; justify-content: center; /* Căn giữa tabs */
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.4rem; font-weight: 800; color: #999; text-transform: uppercase;
        padding: 10px 20px; border-radius: 30px; transition: all 0.3s;
        background: rgba(255,255,255,0.3); /* Nền tab chưa chọn */
    }
    .stTabs [aria-selected="true"] {
        color: white !important; background: #FF1493 !important; /* Nền tab đã chọn */
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.4);
    }

    /* --- FOOTER --- */
    .footer {
        text-align: center; color: #666; padding: 40px 0; margin-top: 40px;
        border-top: 1px solid rgba(255, 20, 147, 0.2);
    }
    .footer h4 { color: #FF1493; font-weight: 800; margin-bottom: 10px; }
    
    /* Ẩn các element thừa của Streamlit */
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 1. NAVBAR (Thanh điều hướng tùy chỉnh bằng HTML/CSS)
# ==============================================================================
st.markdown("""
<div class="nav-container">
    <div class="nav-logo">☀️ AN AN <span>CINEMA</span></div>
    <div class="nav-menu">
        <div class="nav-button">🎫 Khuyến Mãi</div>
        <div class="nav-button">🍿 Rạp & Giá Vé</div>
        <div class="nav-button">👤 Đăng Nhập / Đăng Ký</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. HERO BANNER KHỔNG LỒ (Nâng cấp)
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-overlay"></div> <!-- Lớp phủ tối -->
    <div class="hero-content">
        <div class="hero-tag">⚡ BOM TẤN ĐANG CHIẾU</div>
        <div class="hero-title">DUNE: HÀNH TINH CÁT - PHẦN 2</div>
        <div class="hero-desc">Trải nghiệm điện ảnh đỉnh cao. Cuộc chiến định đoạt số phận vũ trụ trên màn ảnh rộng IMAX tại An An Cinema. Đừng bỏ lỡ!</div>
        <button class="hero-button">▶ XEM TRAILER & ĐẶT VÉ NGAY</button>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. WIDGET MUA VÉ NHANH (Glassmorphism)
# ==============================================================================
# Sử dụng container để áp dụng class CSS tùy chỉnh
with st.container():
    st.markdown('<div class="quick-book-container glass-effect">', unsafe_allow_html=True)
    st.markdown('<div class="quick-book-title">MUA VÉ NHANH</div>', unsafe_allow_html=True)
    
    # Khung chọn nhanh chia 5 cột
    qb1, qb2, qb3, qb4, qb5 = st.columns(5)
    with qb1:
        st.selectbox("🎬 Chọn Phim", ["(Vui lòng chọn phim)", "Dune: Part 2", "Kungfu Panda 4", "Godzilla x Kong", "Exhuma: Quật Mộ"])
    with qb2:
        st.selectbox("🏢 Chọn Rạp", ["(Vui lòng chọn rạp)", "An An IMAX Center", "An An Gold Class", "An An Landmark 81"])
    with qb3:
        st.selectbox("📅 Ngày Xem", ["(Chọn ngày)", "Hôm nay, 28/05", "Ngày mai, 29/05", "Thứ Năm, 30/05"])
    with qb4:
        st.selectbox("⏰ Suất Chiếu", ["(Chọn suất)", "09:30 (IMAX)", "13:15 (2D)", "18:00 (IMAX)", "20:30 (GOLD)", "23:00 (2D)"])
    with qb5:
        # CSS để căn chỉnh nút bấm thẳng hàng với selectbox
        st.write("<div style='margin-top: 28px; height: 100%;'>", unsafe_allow_html=True)
        st.button("TÌM VÉ NGAY", type="primary", use_container_width=True)
        st.write("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Đóng thẻ div quick-book-container


# ==============================================================================
# 4. DANH SÁCH PHIM (Tabs & Cards Glassmorphism)
# ==============================================================================
st.write("")
tabs = st.tabs(["🔥 ĐANG CHIẾU (HOT)", "🎬 SẮP CHIẾU", "💎 RẠP ĐẶC BIỆT"])

with tabs[0]:
    st.write("")
    # Áp dụng class CSS cho toàn bộ vùng chứa các card
    st.markdown('<div class="movie-card-container">', unsafe_allow_html=True)
    cols = st.columns(4)
    
    # --- HÀM TẠO CARD PHIM ĐỂ TÁI SỬ DỤNG ---
    def create_movie_card(col, title, rating, duration, genre, img_url, btn_key):
        with col:
            with st.container():
                # Phần Ảnh (Image Container)
                st.markdown(f"""
                <div class="image-container">
                    <img src="{img_url}" alt="{title}">
                </div>
                """, unsafe_allow_html=True)
                
                # Phần Nội dung (Content Container)
                st.markdown(f"""
                <div class="content-container">
                    <div>
                        <h3>{title}</h3>
                        <div class="movie-info">
                            <div class="movie-rating">⭐ <span>{rating}</span></div>
                            <div>⏱️ {duration}p</div>
                        </div>
                        <div class="movie-genre">🎭 {genre}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Nút bấm (Sử dụng st.button của Streamlit để có tính năng)
                st.markdown('<div class="card-button">', unsafe_allow_html=True)
                if st.button("🎫 ĐẶT VÉ", key=btn_key, use_container_width=True):
                     st.toast(f"Bạn đã chọn phim: {title}! Chức năng đang phát triển.", icon="🎉")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True) # Đóng content-container

    # --- TẠO CÁC CARD PHIM ---
    create_movie_card(cols[0], "Dune: Hành Tinh Cát 2", "9.5", "166", "Viễn tưởng, Hành động, Phiêu lưu",
                      "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&q=80", "btn_dune")
    
    create_movie_card(cols[1], "Kung Fu Panda 4", "8.9", "94", "Hoạt hình, Hài, Gia đình, Võ thuật",
                      "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80", "btn_panda") # Ảnh placeholder

    create_movie_card(cols[2], "Godzilla x Kong: Đế Chế Mới", "9.0", "115", "Hành động, Quái vật, Viễn tưởng",
                      "https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=500&q=80", "btn_gxk")

    create_movie_card(cols[3], "Exhuma: Quật Mộ Trùng Ma", "9.2", "134", "Kinh dị, Bí ẩn, Tâm linh",
                      "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=500&q=80", "btn_exhuma") # Ảnh placeholder

    st.markdown('</div>', unsafe_allow_html=True) # Đóng movie-card-container

# ==============================================================================
# 5. FOOTER
# ==============================================================================
st.write("")
st.write("")
st.divider()

st.markdown("""
<div class="footer">
    <h4>CÔNG TY TNHH AN AN CINEMA ☀️</h4>
    <p>
        Giấy CNĐKDN: 0123456789 - Đăng ký lần đầu: 28/05/2026<br>
        Hotline: 1900 1000 | Email: hotro@anancinema.vn<br>
        Địa chỉ: Tầng 1, Tòa nhà An An Tower, Quận 1, TP.HCM<br>
        © 2026 An An Cinema. All rights reserved.
    </p>
    <p style="margin-top: 15px; font-size: 0.8rem;">
        <a href="#" style="color: #FF1493; text-decoration: none; margin: 0 10px;">Điều khoản sử dụng</a> | 
        <a href="#" style="color: #FF1493; text-decoration: none; margin: 0 10px;">Chính sách bảo mật</a> |
        <a href="#" style="color: #FF1493; text-decoration: none; margin: 0 10px;">Tuyển dụng</a>
    </p>
</div>
""", unsafe_allow_html=True)