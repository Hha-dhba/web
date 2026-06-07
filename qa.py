import streamlit as st

# Cấu hình trang web rộng rãi, giao diện hiện đại
st.set_page_config(page_title="Thời trang tiết kiệm", page_icon="👕", layout="wide")

# --- QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "name": "Phương",
        "coins": 50,
        "is_verified": False,
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
    }

# DATABASE CHUẨN: Hỗ trợ linh hoạt cả link ảnh URL tĩnh và dữ liệu ảnh tải lên trực tiếp
if 'products' not in st.session_state:
    st.session_state.products = [
        # --- NHÓM ÁO KHOÁC / HOODIE (STREETWEAR) ---
        {
            "id": 1, "category": "Áo khoác / Hoodie", "title": "Áo khoác Varsity Jacket Local Brand màu xanh lính phối tay da", "size": "L", "brand": "Bad Habits", 
            "condition": "95% (Chất dạ dày dặn nỉ chần bông, tay da không nổ, mặc đi học mùa đông bao ngầu)", "location": "Hà Nội", "price": 90000, "rating": 5,
            "owner": "Hoàng Long (HUST)", "is_owner_verified": True,
            "image_url": "https://i.pinimg.com/1200x/09/32/46/093246d9b8ba6325c6ef798594ba8b3b.jpg", "uploaded_file": None
        },
        {
            "id": 2, "category": "Áo khoác / Hoodie", "title": "Áo Hoodie xám loang dáng rộng unisex basic nam nữ", "size": "L", "brand": "Dirty Coins", 
            "condition": "92% (Form rộng che khuyết điểm đỉnh kout)", "location": "TP. Hồ Chí Minh", "price": 60000, "rating": 4,
            "owner": "Minh Tú (UEH)", "is_owner_verified": False,
            "image_url": "https://i.pinimg.com/1200x/9d/3e/a2/9d3ea2ad83e2b6b119652d72131e3fdf.jpg", "uploaded_file": None
        },
        {
            "id": 3, "category": "Áo khoác / Hoodie", "title": "Áo blazer nữ", "size": "M", "brand": "Dirty Coins", 
            "condition": "92% (Trang phục công sở)", "location": "Hà Nội", "price": 60000, "rating": 4,
            "owner": "Ánh Dương (UEH)", "is_owner_verified": False,
            "image_url": "https://i.pinimg.com/1200x/1f/ca/55/1fca559c868349354af78e8b9f8277e3.jpg", "uploaded_file": None
        },

        # --- NHÓM ÁO PHÔNG / SƠ MI (CASUAL GOING TO SCHOOL) ---
        {
            "id": 4, "category": "Áo phông / Sơ mi", "title": "Áo thun Baby Tee màu hồng", "size": "S", "brand": "Tobi Streetwear", 
            "condition": "98% (Mới mặc thử 1 lần chụp ảnh tiktok, chất thun bo gân co giãn ôm dáng cực xinh)", "location": "Hà Nội", "price": 0, "rating": 5,
            "owner": "Linh Chi (BA)", "is_owner_verified": True,
            "image_url": "https://i.pinimg.com/1200x/55/df/56/55df563b0df40773fc9686644a98920d.jpg", "uploaded_file": None
        },
        {
            "id": 5, "category": "Áo phông / Sơ mi", "title": "Áo sơ mi kẻ caro", "size": "M", "brand": "Khác", 
            "condition": "90% (Vải thô đũi mát mẻ)", "location": "Hà Nội", "price": 0, "rating": 4,
            "owner": "Khánh Linh (FTU)", "is_owner_verified": True,
            "image_url": "https://i.pinimg.com/1200x/dc/38/3b/dc383b00102e376311b6d740ddcb25d6.jpg", "uploaded_file": None
        },
        {
            "id": 6, "category": "Áo phông / Sơ mi", "title": "Áo sơ mi trắng trơn cotton dài tay basic đi học/đi chơi", "size": "L", "brand": "Uniqlo", 
            "condition": "95% (Vải phẳng phiu phẳng nếp, cam đoan không ố vàng cổ áo, form rộng dễ sơ vin)", "location": "Hà Nội", "price": 55000, "rating": 5,
            "owner": "Tuấn Đạt (NEU)", "is_owner_verified": True,
            "image_url": "https://i.pinimg.com/736x/bd/c1/9b/bdc19b3442f43c9ca788e690009125cd.jpg", "uploaded_file": None
        },

        # --- NHÓM QUẦN JEAN / QUẦN ĐÙI ---
        {
            "id": 7, "category": "Quần Jean", "title": "Quần jean nữ ống rộng dáng suông wash màu xanh rêu bụi bặm", "size": "M", "brand": "Khác", 
            "condition": "80% (Vải denim dày dặn cạp cao hack chân dài, mix với croptop là bao cháy luôn nha b)", "location": "Hà Nội", "price": 70000, "rating": 4,
            "owner": "Phương Thảo", "is_owner_verified": False,
            "image_url": "https://i.pinimg.com/1200x/63/8c/15/638c15b21e50a0df86a962dc3c0d893c.jpg", "uploaded_file": None
        },
        {
            "id": 8, "category": "Quần Jean", "title": "Quần Short Jean nam màu đen khói", "size": "XL", "brand": "Local Brand", 
            "condition": "95% (Chất bò dày dặn)", "location": "Hà Nội", "price": 50000, "rating": 5,
            "owner": "Đức Anh", "is_owner_verified": False,
            "image_url": "https://i.pinimg.com/1200x/11/8e/54/118e54e12a5c0ab02f5a8c39473df31c.jpg", "uploaded_file": None
        },

        # --- NHÓM CHÂN VÁY (GIRLY STYLE) ---
        {
            "id": 9, "category": "Chân váy", "title": "Chân váy ngắn xếp ly màu đen cá tính", "size": "S", "brand": "Local Brand", 
            "condition": "95% (Vải tuyết mưa dày dặn, form xếp ly xòe siêu xinh diện đi học đi chơi đều bốc)", "location": "Hà Nội", "price": 50000, "rating": 5,
            "owner": "Huyền Trang", "is_owner_verified": True,
            "image_url": "https://i.pinimg.com/736x/7c/ac/c0/7cacc04092981a9d66a3cf78eef5a7ad.jpg", "uploaded_file": None
        },
        {
            "id": 10, "category": "Chân váy", "title": "Chân váy ren xòe 3 tầng Coquette tiểu thư màu trắng bánh bèo", "size": "M", "brand": "Khác", 
            "condition": "99% (Mới lướt đúng 1 lần đi cà phê sống ảo chụp ảnh)", "location": "Hà Nội", "price": 35000, "rating": 5,
            "owner": "Quỳnh Anh", "is_owner_verified": False,
            "image_url": "https://i.pinimg.com/1200x/38/42/19/384219501a883677c4113ce290892aee.jpg", "uploaded_file": None
        },

        # --- NHÓM VÁY ĐẦM DỰ TIỆC (PROM / PARTY) ---
        {
            "id": 11, "category": "Váy / Đầm dự tiệc", "title": "Đầm dự tiệc váy lụa satin trắng tiểu thư chảnh lộng lẫy", "size": "S", "brand": "NTV Clothings", 
            "condition": "98% (Pass cực rẻ cho b nào diện đi prom trường hoặc đi đám cưới, mặc lên tôn dáng lắm luôn)", "location": "Hà Nội", "price": 90000, "rating": 5,
            "owner": "Minh Thư", "is_owner_verified": False,
            "image_url": "https://i.pinimg.com/736x/78/97/98/7897987eb4ea23226edeee83c8332ac3.jpg", "uploaded_file": None
        }
    ]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

# --- GIAO DIỆN CHÍNH ---
st.title("THỜI TRANG TIẾT KIỆM")
st.caption("Góc pass đồ quần áo cũ thực tế, không giới hạn số lượng bài đăng của học sinh, sinh viên Việt Nam")

# Thanh trạng thái ví Green Coin
st.markdown(f"🪙 **Ví Green Coin của bạn:** `{st.session_state.user_profile['coins']} Xu` | Thẻ sinh viên: {'✅ Đã xác thực (Tích xanh uy tín)' if st.session_state.user_profile['is_verified'] else '❌ Chưa xác thực'}")

# Khởi tạo các Tab tính năng
tab_home, tab_chat, tab_post, tab_profile = st.tabs([
    "🛒 Lướt đồ ngon (Khám phá)", 
    "💬 Inbox thương lượng (Chat)", 
    "➕ Đăng bài pass đồ", 
    "👤 Thẻ sinh viên & Profile (KYC)"
])

# ==========================================
# TAB 1: KHÁM PHÁ & TRAO ĐỔI
# ==========================================
with tab_home:
    st.subheader("🔍 Tìm kiếm & Bộ lọc quần áo trúng gu")
    
    search_query = st.text_input("Nhập tên quần áo bạn muốn tìm (Ví dụ: Hoodie, Chân váy, Sơ mi...):", placeholder="Gõ đồ cần tìm ở đây...")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        filter_category = st.multiselect("Phân loại trang phục:", ["Áo phông / Sơ mi", "Quần Jean", "Chân váy", "Áo khoác / Hoodie", "Váy / Đầm dự tiệc"])
    with col_f2:
        filter_size = st.multiselect("Chọn Size vừa vặn:", ["S", "M", "L", "XL", "Free size"])
    with col_f3:
        filter_brand = st.multiselect("Phân loại Brand:", ["Bad Habits", "Dirty Coins", "Tobi Streetwear", "Uniqlo", "Khác"])
    with col_f4:
        filter_loc = st.selectbox("Khu vực tiện ship đồ:", ["Tất cả", "Hà Nội", "TP. Hồ Chí Minh"])

    st.markdown("---")

    filtered_products = st.session_state.products
    
    if search_query:
        filtered_products = [p for p in filtered_products if search_query.lower() in p["title"].lower()]
    if filter_category:
        filtered_products = [p for p in filtered_products if p.get("category") in filter_category]
    if filter_size:
        filtered_products = [p for p in filtered_products if p["size"] in filter_size]
    if filter_brand:
        filtered_products = [p for p in filtered_products if p["brand"] in filter_brand]
    if filter_loc != "Tất cả":
        filtered_products = [p for p in filtered_products if p["location"] == filter_loc]

    st.subheader("Danh sách bài đăng pass đồ cũ thực tế")
    
    if not filtered_products:
        st.info("Hết đồ khớp bộ lọc rồi b ơi, b thử tìm từ khóa khác hoặc bỏ bớt tích chọn nhé!")
    else:
        for p in filtered_products:
            # Tạo chuỗi key an toàn tuyệt đối, tránh trùng lặp phần tử
            safe_suffix = f"{p['id']}_{p.get('category', 'item')}"
            
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 3, 2])
                
                with c1:
                    # TÍNH NĂNG THỰC TẾ: Nếu đồ có ảnh tải lên từ máy tính thì ưu tiên hiển thị trước, ngược lại dùng link mẫu
                    if p.get("uploaded_file") is not None:
                        st.image(p["uploaded_file"], use_container_width=True)
                    else:
                        st.image(p["image_url"], use_container_width=True)
                    st.markdown(f"<span style='background-color:#007BFF; color:white; padding:3px 8px; border-radius:10px; font-size:12px;'>🏷️ {p.get('category', 'Quần áo')}</span>", unsafe_allow_html=True)
                
                with c2:
                    verified_badge = "(Sinh viên uy tín)" if p["is_owner_verified"] else ""
                    st.markdown(f"### **{p['title']}**")
                    st.write(f"**Người đăng pass:** {p['owner']} <span style='color:#1D9BF0; font-weight:bold;'>{verified_badge}</span>", unsafe_allow_html=True)
                    st.write(f"**Brand gốc:** {p['brand']} | **Size đồ:** <span style='background-color:#FF4B4B; color:white; padding:2px 6px; border-radius:3px; font-weight:bold;'>{p['size']}</span>", unsafe_allow_html=True)
                    st.write(f"**Tình trạng cũ mới (Cond):** {p['condition']}")
                    st.write(f"**Khu vực ship:** {p['location']}")
                    
                    with st.expander("Bình luận công khai hỏi thông tin đồ"):
                        st.write("*Phuong_HUST:* Cao 1m6 mặc vừa món này không b yêu?")
                        st.text_input("Gõ câu hỏi của b...", key=f"comm_{safe_suffix}")

                with c3:
                    st.markdown(f"<h3 style='color: #2E7D32;'>Giá pass đồ: {p['price']:,} đ</h3>", unsafe_allow_html=True)
                    st.caption("*Cam kết: Giá thanh lý hạt dẻ cho sinh viên học sinh.*")
                    
                    if st.button(f"Inbox thương lượng thêm", key=f"chat_{safe_suffix}", use_container_width=True):
                        st.info("Đã mở phòng chat! B qua Tab 'Inbox thương lượng (Chat)' nha.")
                    
                    with st.popover("💳 Đặt mua & Thanh toán tiền ship", use_container_width=True):
                        st.markdown("#### **Chi tiết đơn hàng**")
                        ship_carrier = st.selectbox("Đơn vị ship liên kết:", ["GHTK (Đồng giá ship sinh viên 22k)", "GHN Nhanh"], key=f"ship_{safe_suffix}")
                        address = st.text_area("Ghi rõ địa chỉ nhận hàng của b nhé:", key=f"addr_{safe_suffix}")
                        
                        ship_cost = 22000 if "GHTK" in ship_carrier else 30000
                        st.write(f"💵 **Giá pass đồ:** {p['price']:,} đ")
                        st.write(f"🚚 **Phí ship đồ:** {ship_cost:,} đ")
                        st.markdown(f"💰 **Tổng giá thanh toán:** <span style='color:red; font-weight:bold; font-size:18px;'>{p['price'] + ship_cost:,} đ</span>", unsafe_allow_html=True)
                        
                        if st.button("Xác nhận đặt hàng luôn", key=f"confirm_{safe_suffix}"):
                            if not address:
                                st.error("Điền địa chỉ nhận hàng đã b ơi!")
                            else:
                                st.session_state.user_profile["coins"] += 50
                                st.success("🎉 Đặt mua thành công! Chờ shipper giao đồ cho b nhé!")
                                st.balloons()
                                st.rerun()

# ==========================================
# TAB 2: INBOX THƯƠNG LƯỢNG (CHAT)
# ==========================================
with tab_chat:
    st.subheader("💬 Phòng chat thương lượng mua đồ")
    chat_users = list(set([p['owner'] for p in st.session_state.products]))
    current_chat_user = st.selectbox("Chọn tài khoản muốn inbox:", chat_users)
    
    if current_chat_user:
        if current_chat_user not in st.session_state.chat_history:
            st.session_state.chat_history[current_chat_user] = [
                {"role": "owner", "text": "Hế lô b nha, đồ mình đảm bảo giống y ảnh thật mình đăng lên á, b cần hỏi size số gì cứ nhắn nha."}
            ]
        
        chat_box = st.container(height=250, border=True)
        with chat_box:
            for msg in st.session_state.chat_history[current_chat_user]:
                if msg["role"] == "user":
                    st.markdown(f"<div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px; float: right; clear: both;'><b>Bạn:</b> {msg['text']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: left; background-color: #EAEAEA; padding: 10px; border-radius: 10px; margin: 5px; float: left; clear: both;'><b>{current_chat_user}:</b> {msg['text']}</div>", unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns([5, 1])
        with col_m1:
            user_msg = st.text_input("Nhập tin nhắn xin fix giá, hỏi size...", key="msg_input", label_visibility="collapsed")
        with col_m2:
            if st.button("Gửi", use_container_width=True) and user_msg:
                st.session_state.chat_history[current_chat_user].append({"role": "user", "text": user_msg})
                st.rerun()

# ==========================================
# TAB 3: ĐĂNG BÀI PASS ĐỒ (CẬP NHẬT TÍNH NĂNG TẢI ẢNH THẬT TỪ MÁY LÊN)
# ==========================================
with tab_post:
    st.subheader("Đăng bài pass món đồ tủ cũ của b")
    st.info("Bạn có thể chụp ảnh thật bằng điện thoại rồi tải file ảnh trực tiếp lên đây, hệ thống sẽ hiển thị ngay lập tức!")

    with st.form("post_form", clear_on_submit=True):
        new_title = st.text_input("Tên món đồ cần pass (VD: Áo hoodie nỉ xám phom rộng, Quần bò suông túi hộp...):")
        
        c_cat, c_size, c_brand, c_loc = st.columns(4)
        with c_cat:
            new_category = st.selectbox("Loại trang phục quần áo:", ["Áo phông / Sơ mi", "Quần Jean", "Chân váy", "Áo khoác / Hoodie", "Váy / Đầm dự tiệc"])
        with c_size:
            new_size = st.selectbox("Size đồ:", ["S", "M", "L", "XL", "Free size"])
        with c_brand:
            new_brand = st.text_input("Brand gốc (nếu có):", placeholder="VD: Dirty Coins, Zara...")
        with c_loc:
            new_loc = st.selectbox("Khu vực b đang ở:", ["Hà Nội", "TP. Hồ Chí Minh"])
            
        new_cond = st.select_slider("Tình trạng thực tế (Cond đồ):", options=["50%", "60%", "70%", "80%", "90%", "95%", "99% (Mới lướt nguyên tag)"])
        new_price = st.number_input("Giá muốn pass đồ mong muốn (đ):", min_value=0, value=50000, step=5000)
        
        # CẢI TIẾN LỚN: Cho phép up file ảnh trực tiếp thay vì nhập link thủ công
        st.markdown("📸 **Tải ảnh chụp thật sản phẩm từ máy tính/điện thoại:**")
        uploaded_prod_image = st.file_uploader("Chọn tệp ảnh quần áo của bạn (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

        submit_btn = st.form_submit_button("Đăng bài lên sàn ngay lập tức")
        
        if submit_btn:
            if not new_title:
                st.error("Quên điền tên sản phẩm kìa b ơi!")
            elif uploaded_prod_image is None:
                st.error("B ơi, chụp tấm ảnh thật của đồ rồi tải lên để các b khác dễ chốt đơn nha!")
            else:
                # Đọc dữ liệu binary của ảnh để hiển thị trực tiếp
                image_bytes = uploaded_prod_image.read()
                
                new_item = {
                    "id": len(st.session_state.products) + 1,
                    "category": new_category,
                    "title": new_title,
                    "size": new_size,
                    "brand": new_brand if new_brand else "Khác",
                    "condition": f"{new_cond} (Ảnh chụp thực tế chính chủ)",
                    "location": new_loc,
                    "price": new_price,
                    "rating": 5,
                    "owner": f"{st.session_state.user_profile['name']} (Tôi)",
                    "is_owner_verified": st.session_state.user_profile["is_verified"],
                    "image_url": "", # Link URL trống vì dùng file tải trực tiếp
                    "uploaded_file": image_bytes # Lưu dữ liệu ảnh vào session state
                }
                st.session_state.products.insert(0, new_item)
                st.success(f"🎉 Món '{new_title}' kèm ảnh chụp thật đã được cập nhật thành công lên trang chủ!")
                st.balloons()
                st.rerun()

# ==========================================
# TAB 4: THẺ SINH VIÊN & PROFILE (KYC)
# ==========================================
with tab_profile:
    st.subheader("👤 Hồ sơ cá nhân & Xác thực Thẻ sinh viên")
    col_p1, col_p2 = st.columns([1, 3])
    with col_p1:
        st.image(st.session_state.user_profile["avatar"], width=130, caption="Avatar của b")
    with col_p2:
        st.markdown(f"### Thành viên: **{st.session_state.user_profile['name']}**")
        st.markdown(f"🪙 Số dư ví Green Coin: <span style='color:#FF4B4B; font-weight:bold; font-size:20px;'>{st.session_state.user_profile['coins']} Xu</span>", unsafe_allow_html=True)
        if st.session_state.user_profile["is_verified"]:
            st.success("✅ Tài khoản đã xác thực DANH TÍNH SINH VIÊN UY TÍN. Đăng đồ tự có tích xanh xịn đét!")
        else:
            st.error("❌ Tài khoản thường. Hãy nộp ảnh Thẻ sinh viên bên dưới để nhận tích xanh uy tín nhé.")

    st.markdown("---")
    st.markdown("#### Cổng up Thẻ sinh viên lấy tích xanh chống lừa đảo")
    if st.session_state.user_profile["is_verified"]:
        st.info("Hệ thống đã phê duyệt Thẻ sinh viên của b thành công, không cần nộp lại nha.")
    else:
        with st.form("kyc_form"):
            st.write("Chụp ảnh mặt trước Thẻ sinh viên của b để hệ thống duyệt nick chính chủ:")
            kyc_file = st.file_uploader("Tải tệp ảnh thẻ lên đây (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
            agree = st.checkbox("Tôi cam kết mô tả đúng tình trạng thật của đồ cũ, không lừa đảo tráo hàng nát.")
            
            submit_kyc = st.form_submit_button("Gửi phê duyệt Thẻ sinh viên")
            if submit_kyc:
                if not kyc_file or not agree:
                    st.error("B ơi, chọn ảnh thẻ rồi tích chọn cam kết uy tín nha.")
                else:
                    st.session_state.user_profile["is_verified"] = True
                    st.success("🎉 Xác thực thành công! B đã chính thức nhận dấu Tích xanh Sinh viên Uy Tín ✅!")
                    st.balloons()
                    st.rerun()

