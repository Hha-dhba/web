import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="EcoSwap ♻️ | Nền tảng trao đổi quần áo",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DỮ LIỆU MẪU (MOCK DATA)
# ==========================================
# Trong thực tế, dữ liệu này sẽ được lấy từ Database (SQL, Firebase,...)
if 'clothing_items' not in st.session_state:
    st.session_state.clothing_items = [
        {
            "id": 1,
            "title": "Áo khoác Denim Vintage",
            "category": "Áo khoác",
            "size": "M",
            "color": "Xanh dương",
            "condition": "90% (Ít mặc)",
            "want_to_swap": "Áo thun oversize hoặc Quần ống rộng",
            "image": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=500&q=80",
            "owner": "Mai Anh"
        },
        {
            "id": 2,
            "title": "Váy hoa nhí mùa hè",
            "category": "Váy/Đầm",
            "size": "S",
            "color": "Vàng",
            "condition": "Mới 100% (Nguyên tag)",
            "want_to_swap": "Túi xách tote hoặc sách",
            "image": "https://images.unsplash.com/photo-1572804013309-82a89b43af28?w=500&q=80",
            "owner": "Linh Đan"
        },
        {
            "id": 3,
            "title": "Áo thun Graphic basic",
            "category": "Áo thun",
            "size": "L",
            "color": "Đen",
            "condition": "80% (Có sờn nhẹ)",
            "want_to_swap": "Bất cứ thứ gì thú vị",
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80",
            "owner": "Hoàng Nam"
        },
        {
            "id": 4,
            "title": "Quần Jeans ống suông",
            "category": "Quần",
            "size": "M",
            "color": "Xanh nhạt",
            "condition": "95% (Mặc 1-2 lần)",
            "want_to_swap": "Áo sơ mi Flannel size L",
            "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&q=80",
            "owner": "Trang NT"
        },
        {
            "id": 5,
            "title": "Áo Len Cardigan Dày",
            "category": "Áo khoác",
            "size": "XL",
            "color": "Be",
            "condition": "85% (Qua 1 mùa đông)",
            "want_to_swap": "Giày Sneaker size 38",
            "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&q=80",
            "owner": "Thúy Vi"
        }
    ]

# ==========================================
# 3. CSS LÀM ĐẸP GIAO DIỆN
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    
    /* Màu nền tươi sáng, thiên nhiên */
    .stApp {
        background-color: #F7F9F6;
        color: #2E3B32;
    }
    
    /* Tùy chỉnh Header/Banner */
    .hero-banner {
        background: linear-gradient(135deg, #A8E6CF 0%, #DCEDC1 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(168, 230, 207, 0.3);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #1A4A38;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #3D6A53;
        font-weight: 600;
    }

    /* Thẻ Sản phẩm (Item Card) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border-radius: 16px;
        border: 1px solid #EAEAEA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        overflow: hidden;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(168, 230, 207, 0.4);
        border-color: #A8E6CF;
    }

    /* Định dạng hình ảnh trong card */
    .img-container {
        width: 100%;
        height: 250px;
        overflow: hidden;
        border-radius: 15px 15px 0 0;
        margin-bottom: 10px;
    }
    .img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Các Tag Size và Màu sắc */
    .tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .tag-size { background-color: #E3F2FD; color: #1565C0; }
    .tag-color { background-color: #FFF3E0; color: #E65100; }
    .tag-cond { background-color: #E8F5E9; color: #2E7D32; }
    
    /* Nút Trao Đổi */
    .stButton > button[kind="primary"] {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.2s;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #43A047;
        box-shadow: 0 4px 10px rgba(76, 175, 80, 0.4);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. SIDEBAR - BỘ LỌC TÌM KIẾM
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3258/3258499.png", width=80)
    st.markdown("<h2 style='color:#2E7D32;'>Bộ Lọc Quần Áo</h2>", unsafe_allow_html=True)
    st.markdown("Tìm món đồ phù hợp với bạn!")
    st.divider()
    
    # Các Widget Lọc
    search_query = st.text_input("🔍 Tìm kiếm tên đồ...")
    
    category_filter = st.multiselect("👗 Thể loại", ["Áo thun", "Áo khoác", "Quần", "Váy/Đầm", "Phụ kiện"])
    
    size_filter = st.multiselect("📏 Kích cỡ (Size)", ["XS", "S", "M", "L", "XL", "Freesize"])
    
    color_filter = st.multiselect("🎨 Màu sắc", ["Đen", "Trắng", "Xanh dương", "Xanh lá", "Vàng", "Đỏ", "Be"])
    
    st.divider()
    st.markdown("<p style='text-align:center; color:#888; font-size:0.8rem;'>Cộng đồng trao đổi đồ cũ EcoSwap</p>", unsafe_allow_html=True)


# ==========================================
# 5. XỬ LÝ LỌC DỮ LIỆU
# ==========================================
filtered_items = st.session_state.clothing_items

# Lọc theo tên
if search_query:
    filtered_items = [item for item in filtered_items if search_query.lower() in item['title'].lower()]

# Lọc theo thể loại
if category_filter:
    filtered_items = [item for item in filtered_items if item['category'] in category_filter]

# Lọc theo size
if size_filter:
    filtered_items = [item for item in filtered_items if item['size'] in size_filter]

# Lọc theo màu
if color_filter:
    filtered_items = [item for item in filtered_items if item['color'] in color_filter]


# ==========================================
# 6. GIAO DIỆN CHÍNH (MAIN CONTENT)
# ==========================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">♻️ EcoSwap</div>
    <div class="hero-subtitle">Đừng vứt đi! Hãy trao đổi để làm mới tủ đồ của bạn và bảo vệ môi trường.</div>
</div>
""", unsafe_allow_html=True)

# Chia Tabs
tab1, tab2, tab3 = st.tabs(["🛒 Tủ Đồ Chung", "➕ Đăng Đồ Trao Đổi", "💬 Tin Nhắn Của Tôi"])

# ------------------------------------------
# TAB 1: HIỂN THỊ DANH SÁCH QUẦN ÁO
# ------------------------------------------
with tab1:
    st.subheader("Những món đồ đang tìm chủ mới")
    
    if len(filtered_items) == 0:
        st.warning("Tiếc quá! Không tìm thấy món đồ nào phù hợp với bộ lọc của bạn.")
    else:
        # Hiển thị dạng lưới 3 cột
        cols = st.columns(3)
        for index, item in enumerate(filtered_items):
            # Tính toán vị trí cột (0, 1, 2)
            col = cols[index % 3]
            
            with col:
                with st.container(border=True):
                    # Hình ảnh
                    st.markdown(f"""
                    <div class="img-container">
                        <img src="{item['image']}" alt="{item['title']}">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tên đồ và người đăng
                    st.markdown(f"<h3 style='margin:0; font-size:1.2rem; color:#1A4A38;'>{item['title']}</h3>", unsafe_allow_html=True)
                    st.caption(f"👤 Đăng bởi: **{item['owner']}**")
                    
                    # Các Tags thông tin (Size, Màu, Độ mới)
                    st.markdown(f"""
                    <div style="margin-top: 10px; margin-bottom: 10px;">
                        <span class="tag tag-size">📏 Size: {item['size']}</span>
                        <span class="tag tag-color">🎨 {item['color']}</span><br>
                        <span class="tag tag-cond">✨ {item['condition']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='font-size:0.9rem; color:#555;'><b>🔄 Muốn đổi lấy:</b> {item['want_to_swap']}</p>", unsafe_allow_html=True)
                    
                    # Nút bấm hành động
                    if st.button("🤝 YÊU CẦU TRAO ĐỔI", key=f"swap_{item['id']}", type="primary", use_container_width=True):
                        st.success(f"Đã gửi yêu cầu trao đổi đến {item['owner']}!")

# ------------------------------------------
# TAB 2: FORM ĐĂNG ĐỒ TỪ NGƯỜI DÙNG
# ------------------------------------------
with tab2:
    st.subheader("Đóng góp vào tủ đồ chung")
    st.write("Điền thông tin món đồ bạn không còn sử dụng để tìm kiếm cơ hội đổi lấy món đồ yêu thích khác nhé!")
    
    with st.form("upload_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            new_title = st.text_input("Tên món đồ", placeholder="VD: Áo sơ mi caro Zara")
            new_cat = st.selectbox("Thể loại", ["Áo thun", "Áo sơ mi", "Áo khoác", "Quần", "Váy/Đầm", "Giày dép", "Phụ kiện"])
            new_size = st.selectbox("Kích cỡ (Size)", ["XS", "S", "M", "L", "XL", "Freesize"])
            new_color = st.text_input("Màu sắc", placeholder="VD: Trắng, Xanh navy...")
            
        with col2:
            new_cond = st.selectbox("Tình trạng / Độ mới", ["Mới 100% (Nguyên tag)", "95% (Mặc 1-2 lần)", "90% (Ít mặc)", "80% (Có sờn nhẹ)", "Cũ (Vintage)"])
            new_swap = st.text_area("Bạn muốn đổi lấy gì?", placeholder="VD: Muốn đổi lấy áo khoác dù size L, hoặc sách tiểu thuyết...", height=115)
            
        st.markdown("---")
        new_img = st.file_uploader("Tải lên hình ảnh sản phẩm (Khuyến khích chụp thực tế)", type=['jpg', 'png', 'jpeg'])
        
        submitted = st.form_submit_button("📤 ĐĂNG TẢI LÊN ECOSWAP", type="primary")
        
        if submitted:
            if new_title and new_color and new_swap:
                # Tạo mục mới và thêm vào session_state (Database giả lập)
                new_item = {
                    "id": len(st.session_state.clothing_items) + 1,
                    "title": new_title,
                    "category": new_cat,
                    "size": new_size,
                    "color": new_color,
                    "condition": new_cond,
                    "want_to_swap": new_swap,
                    "image": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=500&q=80", # Ảnh mặc định khi upload
                    "owner": "Bạn (Người dùng hiện tại)"
                }
                st.session_state.clothing_items.append(new_item)
                st.success("Tuyệt vời! Món đồ của bạn đã được đăng lên Tủ Đồ Chung.")
                st.balloons()
            else:
                st.error("Vui lòng điền đầy đủ các thông tin bắt buộc (Tên đồ, Màu sắc, Muốn đổi lấy)!")

# ------------------------------------------
# TAB 3: CHỨC NĂNG PHÁT TRIỂN THÊM
# ------------------------------------------
with tab3:
    st.subheader("Hộp thư của bạn")
    st.info("Tính năng nhắn tin và thương lượng trao đổi trực tiếp giữa các người dùng đang được phát triển. Vui lòng quay lại sau!")
    
    st.image("https://illustrations.popsy.co/amber/communication.svg", width=300)