import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')

# Color Palette
COLOR_PRIMARY = RGBColor(27, 54, 93)      # Dark Navy
COLOR_SECONDARY = RGBColor(43, 84, 126)   # Steel Blue
COLOR_ACCENT = RGBColor(0, 122, 255)      # Bright Blue
COLOR_BG_LIGHT = RGBColor(248, 250, 252)  # Slate 50
COLOR_CARD_BG = RGBColor(255, 255, 255)   # White
COLOR_TEXT_DARK = RGBColor(30, 41, 59)    # Slate 800
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)# Slate 500
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_SUCCESS = RGBColor(16, 185, 129)    # Emerald

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    def add_header(slide, title_text, category_text="BÀI TẬP LỚN MÔN HỌC MÁY CƠ BẢN - NHÓM 15"):
        # Category / Banner Top
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY

        # Dividing Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.color.rgb = RGBColor(226, 232, 240)

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=RGBColor(226, 232, 240)):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: Title Slide (Bìa)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY
    bg1.line.fill.background()

    # Title Card Inner
    add_card(slide1, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), bg_color=RGBColor(255, 255, 255))

    # Badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.5), Inches(3.2), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(238, 242, 255)
    badge.line.color.rgb = COLOR_ACCENT
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "BÁO CÁO HỌC THUẬT & SẢN PHẨM"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_ACCENT
    p_b.alignment = PP_ALIGN.CENTER

    # Main Title Text
    tb1 = slide1.shapes.add_textbox(Inches(1.5), Inches(2.1), Inches(10.3), Inches(1.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "PHÂN LOẠI PHÂN KHÚC GIÁ ĐIỆN THOẠI THÔNG MINH"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY
    
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Mobile Price Classification — Microservices Architecture & Docker Deployment"
    p1_sub.font.size = Pt(16)
    p1_sub.font.color.rgb = COLOR_TEXT_MUTED
    p1_sub.space_before = Pt(8)

    # Details Box (Group info)
    tb_info = slide1.shapes.add_textbox(Inches(1.5), Inches(4.2), Inches(10.3), Inches(1.8))
    tf_info = tb_info.text_frame
    tf_info.word_wrap = True
    
    infos = [
        ("Tên Nhóm:", "Nhóm 15"),
        ("Thành Viên:", "SV1: 10123334 (EDA, Pipeline, Models)  |  SV2: 10123343 (FastAPI, Docker, UI, Tests)"),
        ("Mô Hình Sản Xuất:", "Logistic Regression Pipeline (Test Accuracy: 97.50%, Macro F1: 97.50%)"),
        ("Kiến Trúc & Đóng Gói:", "Microservices 4 Container (Frontend Nginx, Backend FastAPI, AI Service, MongoDB)")
    ]
    for lbl, val in infos:
        pi = tf_info.add_paragraph()
        pi.space_before = Pt(4)
        r_lbl = pi.add_run()
        r_lbl.text = f"{lbl} "
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(13)
        r_lbl.font.color.rgb = COLOR_PRIMARY
        
        r_val = pi.add_run()
        r_val.text = val
        r_val.font.size = Pt(13)
        r_val.font.color.rgb = COLOR_TEXT_DARK
        if "Accuracy" in val:
            r_val.font.bold = True
            r_val.font.color.rgb = COLOR_SUCCESS

    # ==========================================
    # SLIDE 2: Section 1 - Bài toán & Dữ liệu
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Giới Thiệu Bài Toán & Bộ Dữ Liệu (Kaggle Benchmark)")

    # Left Card: Overview
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    tb_s2_left = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_s2_l = tb_s2_left.text_frame
    tf_s2_l.word_wrap = True
    
    p = tf_s2_l.paragraphs[0]
    p.text = "TỔNG QUAN BÀI TOÁN"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_PRIMARY
    
    add_bullets_s2_l = [
        ("Loại bài toán:", "Phân loại đa lớp có giám sát (Multiclass Classification)."),
        ("Nguồn dữ liệu:", "Kaggle Benchmark (Tác giả Abhishek Sharma, giấy phép ODbL/CC0 public domain)."),
        ("Quy mô tập dữ liệu:", "2,000 mẫu huấn luyện (`train.csv`) và 1,000 mẫu kiểm thử (`test.csv`). Sạch 100% (0 missing values)."),
        ("Biến mục tiêu `price_range`:", "Gồm 4 phân khúc khoảng giá cân bằng hoàn hảo (500 mẫu/lớp = 25.0%):"),
        ("  • Lớp 0 (Low Cost):", "Phổ thông giá rẻ (< 3 triệu VNĐ)."),
        ("  • Lớp 1 (Medium Cost):", "Tầm trung (3 - 7 triệu VNĐ)."),
        ("  • Lớp 2 (High Cost):", "Cận cao cấp (7 - 12 triệu VNĐ)."),
        ("  • Lớp 3 (Very High Cost):", "Flagship / Cao cấp (> 12 triệu VNĐ).")
    ]
    for b_title, b_desc in add_bullets_s2_l:
        pi = tf_s2_l.add_paragraph()
        pi.space_before = Pt(4)
        r1 = pi.add_run()
        r1.text = b_title + " "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_SECONDARY
        r2 = pi.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_DARK

    # Right Card: 4 Hardware Feature Groups
    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    tb_s2_right = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_s2_r = tb_s2_right.text_frame
    tf_s2_r.word_wrap = True
    
    p = tf_s2_r.paragraphs[0]
    p.text = "DANH MỤC 20 ĐẶC TRƯNG ĐẦU VÀO"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_PRIMARY
    
    groups_data = [
        ("1. Hiệu Năng & Bộ Nhớ", "ram (256-3998 MB), int_memory (2-64 GB), n_cores (1-8), clock_speed (0.5-3.0 GHz)."),
        ("2. Pin & Nguồn Năng Lượng", "battery_power (501-1998 mAh), talk_time (2-20 giờ đàm thoại)."),
        ("3. Màn Hình & Kích Thước", "px_height (0-1960 px), px_width (500-1998 px), sc_h/sc_w (cm), m_dep (cm), mobile_wt (80-200g), touch_screen (0/1)."),
        ("4. Camera & Kết Nối Mạng", "pc (0-20 MP), fc (0-19 MP), blue (0/1), dual_sim (0/1), three_g (0/1), four_g (0/1), wifi (0/1).")
    ]
    for g_title, g_desc in groups_data:
        pi = tf_s2_r.add_paragraph()
        pi.space_before = Pt(8)
        r1 = pi.add_run()
        r1.text = g_title + "\n"
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_ACCENT
        r2 = pi.add_run()
        r2.text = g_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_TEXT_DARK

    # ==========================================
    # SLIDE 3: Section 2 - EDA (Biến mục tiêu & RAM)
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Phân Tích Khám Phá Dữ Liệu EDA (Phân Phối Lớp & RAM)")

    # 3 Column Images / Analysis
    # Image 1: Target Distribution
    add_card(slide3, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3))
    if os.path.exists("docs/figures/01_target_distribution.png"):
        slide3.shapes.add_picture("docs/figures/01_target_distribution.png", Inches(0.9), Inches(1.7), width=Inches(3.5))
    tb_eda1 = slide3.shapes.add_textbox(Inches(0.9), Inches(4.3), Inches(3.5), Inches(2.5))
    tf_e1 = tb_eda1.text_frame
    tf_e1.word_wrap = True
    p = tf_e1.paragraphs[0]
    p.text = "Hình 1: Biến Mục Tiêu"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    p_desc = tf_e1.add_paragraph()
    p_desc.text = "• 500 mẫu/lớp (25.0% đều).\n• Baseline ngẫu nhiên: 25.0%.\n• Không cần xử lý SMOTE/Oversampling. Áp dụng Stratified Split."
    p_desc.font.size = Pt(10)

    # Image 2: Heatmap
    add_card(slide3, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3))
    if os.path.exists("docs/figures/02_correlation_heatmap.png"):
        slide3.shapes.add_picture("docs/figures/02_correlation_heatmap.png", Inches(4.9), Inches(1.7), width=Inches(3.5))
    tb_eda2 = slide3.shapes.add_textbox(Inches(4.9), Inches(4.3), Inches(3.5), Inches(2.5))
    tf_e2 = tb_eda2.text_frame
    tf_e2.word_wrap = True
    p = tf_e2.paragraphs[0]
    p.text = "Hình 2: Ma Trận Tương Quan"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    p_desc = tf_e2.add_paragraph()
    p_desc.text = "• RAM tương quan mạnh nhất (r = 0.917).\n• Battery & Pixel tương quan vừa (r ~ 0.15 - 0.20).\n• Đa cộng tuyến an toàn (max r = 0.64 giữa pc & fc)."
    p_desc.font.size = Pt(10)

    # Image 3: RAM vs Price
    add_card(slide3, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3))
    if os.path.exists("docs/figures/03_ram_vs_price.png"):
        slide3.shapes.add_picture("docs/figures/03_ram_vs_price.png", Inches(8.9), Inches(1.7), width=Inches(3.5))
    tb_eda3 = slide3.shapes.add_textbox(Inches(8.9), Inches(4.3), Inches(3.5), Inches(2.5))
    tf_e3 = tb_eda3.text_frame
    tf_e3.word_wrap = True
    p = tf_e3.paragraphs[0]
    p.text = "Hình 3: RAM vs Price Range"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    p_desc = tf_e3.add_paragraph()
    p_desc.text = "• Các hộp IQR tách biệt rõ nét theo bậc thang.\n• Tạo ranh giới siêu phẳng tuyến tính tuyệt vời.\n• Không xuất hiện điểm dị biệt ngoại lai."
    p_desc.font.size = Pt(10)

    # ==========================================
    # SLIDE 4: Section 2 - EDA (Pin, Màn hình, Kết nối & Trọng số)
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "2. Phân Tích Khám Phá Dữ Liệu EDA (Pin, Màn Hình & Trọng Số)")

    # 3 Column Images
    # Image 4: Battery & Resolution
    add_card(slide4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3))
    if os.path.exists("docs/figures/04_battery_and_resolution.png"):
        slide4.shapes.add_picture("docs/figures/04_battery_and_resolution.png", Inches(0.9), Inches(1.7), width=Inches(3.5))
    tb_eda4 = slide4.shapes.add_textbox(Inches(0.9), Inches(4.3), Inches(3.5), Inches(2.5))
    tf_e4 = tb_eda4.text_frame
    tf_e4.word_wrap = True
    p = tf_e4.paragraphs[0]
    p.text = "Hình 4: Pin & Độ Phân Giải"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    p_desc = tf_e4.add_paragraph()
    p_desc.text = "• Máy cao cấp (Lớp 2 & 3) tập trung ở góc pin > 1200 mAh & màn hình > 1.5M px.\n• Yếu tố phần cứng quan trọng thứ nhì sau RAM."
    p_desc.font.size = Pt(10)

    # Image 5: Connectivity
    add_card(slide4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3))
    if os.path.exists("docs/figures/05_connectivity_distribution.png"):
        slide4.shapes.add_picture("docs/figures/05_connectivity_distribution.png", Inches(4.9), Inches(1.7), width=Inches(3.5))
    tb_eda5 = slide4.shapes.add_textbox(Inches(4.9), Inches(4.3), Inches(3.5), Inches(2.5))
    tf_e5 = tb_eda5.text_frame
    tf_e5.word_wrap = True
    p = tf_e5.paragraphs[0]
    p.text = "Hình 5: Chuẩn Kết Nối"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    p_desc = tf_e5.add_paragraph()
    p_desc.text = "• 3G phổ cập > 75% ở mọi phân khúc.\n• 4G, Wifi, Bluetooth, 2 SIM xuất hiện đồng đều 50-55%.\n• Thiết kế toggle switch trên UI."
    p_desc.font.size = Pt(10)

    # Image 8: Feature Importance
    add_card(slide4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3))
    if os.path.exists("docs/figures/08_feature_importance.png"):
        slide4.shapes.add_picture("docs/figures/08_feature_importance.png", Inches(8.9), Inches(1.7), width=Inches(3.5))
    tb_eda8 = slide4.shapes.add_textbox(Inches(8.9), Inches(4.3), Inches(3.5), Inches(2.5))
    tf_e8 = tb_eda8.text_frame
    tf_e8.word_wrap = True
    p = tf_e8.paragraphs[0]
    p.text = "Hình 8: Trọng Số Đặc Trưng"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    p_desc = tf_e8.add_paragraph()
    p_desc.text = "• RAM chiếm > 45% trọng số phân loại.\n• Battery & Độ phân giải màn hình chiếm ~25%.\n• Ưu tiên nhóm Hiệu năng & Nguồn trên UI."
    p_desc.font.size = Pt(10)

    # ==========================================
    # SLIDE 5: Section 3 - Xử lý dữ liệu
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "3. Quy Trình Tiền Xử Lý Dữ Liệu & Chống Rò Rỉ (No Data Leakage)")

    # 4 Steps Cards
    steps = [
        ("Bước 1: Phân Chia Stratified Split 80/20", "Phân chia 1,600 mẫu Train (80%) và 400 mẫu Test (20%) với `random_state=42`.\nÁp dụng `stratify=y` bảo toàn chính xác tỷ lệ 25.0% đồng đều của 4 phân khúc giá trên cả 2 tập."),
        ("Bước 2: StandardScaler (Chống Data Leakage)", "Tính toán trung bình ($\mu$) và độ lệch chuẩn ($\sigma$) DUY NHẤT trên tập Train (`scaler.fit(X_train)`).\nSau đó mới biến đổi `transform` sang tập Test. Tuyệt đối không fit trên tập Test."),
        ("Bước 3: Đóng Gói Scikit-Learn Pipeline", "Tích hợp Preprocessor (`StandardScaler`) và Classifier vào trong 1 `Pipeline` duy nhất.\nDữ liệu mới khi predict sẽ tự động được chuẩn hóa thang đo chuẩn từ tập Train."),
        ("Bước 4: Định Nghĩa Schema Ràng Buộc (`schema.json`)", "Định nghĩa chuẩn tên 20 đặc trưng, kiểu dữ liệu, khoảng giá trị hợp lệ [min, max] và nhãn tiếng Việt.\nDùng chung kiểm thực ở Backend FastAPI và dựng form Frontend.")
    ]
    
    positions = [(0.8, 1.6), (6.8, 1.6), (0.8, 4.4), (6.8, 4.4)]
    for idx, (title, body) in enumerate(steps):
        left, top = positions[idx]
        add_card(slide5, Inches(left), Inches(top), Inches(5.7), Inches(2.5))
        tb = slide5.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.2), Inches(5.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY
        
        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_TEXT_DARK
        p_b.space_before = Pt(4)

    # ==========================================
    # SLIDE 6: Section 4 - Các mô hình học máy
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "4. Thử Nghiệm & Siêu Tham Số Các Mô Hình Học Máy")

    models_info = [
        ("🏆 1. Logistic Regression (Multinomial)", "• Nguyên lý: Hàm Softmax ước lượng xác suất 4 lớp $P(y=k|X) = \\frac{e^{w_k^T X + b_k}}{\\sum e^{w_j^T X + b_j}}$.\n• Siêu tham số thử nghiệm: $C \\in [0.01, 0.1, 1.0, 10.0, 100.0]$, solver='lbfgs', max_iter=1000.\n• Kết quả tinh chỉnh: $C = 10.0$ cho hiệu năng tối ưu nhất (5-Fold CV Score = 96.31%)."),
        ("🥈 2. Support Vector Machine (SVC)", "• Nguyên lý: Tìm kiếm siêu phẳng tối ưu (Optimal Hyperplane) tối đa hóa khoảng cách biên (Margin).\n• Siêu tham số thử nghiệm: $C \\in [0.1, 1.0, 5.0, 10.0]$, kernel='linear' & 'rbf'.\n• Kết quả tinh chỉnh: Linear Kernel với $C = 5.0$ cho hiệu năng rất tốt (5-Fold CV Score = 95.81%)."),
        ("🥉 3. Naive Bayes (Gaussian NB)", "• Nguyên lý: Giả định các đặc trưng độc lập khi biết lớp. Làm baseline đánh giá xác suất.\n• Siêu tham số thử nghiệm: `var_smoothing` từ $1e-9$ đến $1e-5$.\n• Kết quả tinh chỉnh: `var_smoothing = 1e-9` (5-Fold CV Score = 80.37%)."),
        ("4. K-Nearest Neighbors (KNN)", "• Nguyên lý: Phân loại dựa trên phiếu bầu lân cận khoảng cách Euclidean.\n• Siêu tham số thử nghiệm: Số lân cận $k \\in [3, 5, 7, 9, 11, 15]$, weights=('uniform', 'distance').\n• Kết quả tinh chỉnh: $k = 11$, `weights='distance'` (5-Fold CV Score = 56.06%).")
    ]

    positions6 = [(0.8, 1.6), (6.8, 1.6), (0.8, 4.4), (6.8, 4.4)]
    for idx, (m_title, m_body) in enumerate(models_info):
        left, top = positions6[idx]
        is_winner = idx == 0
        bg_c = RGBColor(238, 242, 255) if is_winner else COLOR_CARD_BG
        border_c = COLOR_ACCENT if is_winner else RGBColor(226, 232, 240)
        
        add_card(slide6, Inches(left), Inches(top), Inches(5.7), Inches(2.5), bg_color=bg_c, border_color=border_c)
        tb = slide6.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(5.3), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY if not is_winner else COLOR_ACCENT
        
        p_b = tf.add_paragraph()
        p_b.text = m_body
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = COLOR_TEXT_DARK
        p_b.space_before = Pt(4)

    # ==========================================
    # SLIDE 7: Section 5 - Đánh giá & So sánh mô hình
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "5. Đánh Giá Hiệu Năng & Lựa Chọn Mô Hình Sản Xuất")

    # Left: Model Comparison Table
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.3))
    tb_tbl_title = slide7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(7.1), Inches(0.4))
    tf_tt = tb_tbl_title.text_frame
    p = tf_tt.paragraphs[0]
    p.text = "BẢNG SO SÁNH CHỈ SỐ METRIC 4 MÔ HÌNH HỌC MÁY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY

    # Add Table
    table_shape = slide7.shapes.add_table(7, 6, Inches(1.0), Inches(2.2), Inches(7.1), Inches(4.5))
    table = table_shape.table
    
    headers7 = ["Mô Hình", "5-Fold CV", "Train Acc", "Test Acc", "Macro F1", "Đánh Giá"]
    widths7 = [Inches(2.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.5)]
    for i, w in enumerate(widths7):
        table.columns[i].width = w
        
    for i, h in enumerate(headers7):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    data7 = [
        ("Logistic Regression", "96.31%", "98.25%", "97.50%", "97.50%", "🏆 Chọn sản xuất"),
        ("SVM (Linear SVC)", "95.81%", "98.19%", "96.50%", "96.50%", "Hiệu năng tốt"),
        ("Gradient Boosting", "89.50%", "100.0%", "92.00%", "91.98%", "Overfitting"),
        ("Random Forest", "87.44%", "100.0%", "89.00%", "88.94%", "Overfitting"),
        ("Naive Bayes (Gaussian)", "80.37%", "81.87%", "81.00%", "81.05%", "Trung bình"),
        ("KNN (k=11)", "56.06%", "100.0%", "57.50%", "57.76%", "Hiệu năng kém")
    ]
    for row_idx, row_values in enumerate(data7):
        for col_idx, text in enumerate(row_values):
            cell = table.cell(row_idx + 1, col_idx)
            is_winner = row_idx == 0
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(238, 242, 255) if is_winner else (RGBColor(248, 250, 252) if row_idx % 2 == 0 else COLOR_WHITE)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
            if is_winner:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT

    # Right: Confusion Matrix & Rationale
    add_card(slide7, Inches(8.5), Inches(1.6), Inches(4.0), Inches(5.3))
    if os.path.exists("docs/figures/07_confusion_matrix.png"):
        slide7.shapes.add_picture("docs/figures/07_confusion_matrix.png", Inches(8.6), Inches(1.7), width=Inches(3.8))
    
    tb_rat = slide7.shapes.add_textbox(Inches(8.6), Inches(4.4), Inches(3.8), Inches(2.4))
    tf_r = tb_rat.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "LÝ DO CHỌN LOGISTIC REGRESSION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    
    p_b = tf_r.add_paragraph()
    p_b.text = "1. Độ chính xác cao nhất (97.50%).\n2. Không bị quá khớp (chênh lệch Train - Test chỉ 0.75%).\n3. File siêu nhẹ (2.1 KB), latency < 5ms.\n4. Ma trận nhầm lẫn: 100% nhầm ở ranh giới lớp liền kề, không nhảy cóc."
    p_b.font.size = Pt(10)

    # ==========================================
    # SLIDE 8: Section 6 - Đóng gói mô hình
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "6. Đóng Gói Mô Hình & Quy Trình Export Model Artifacts")

    # 3 Column Cards
    artifacts_info = [
        ("1. Tệp Model Pipeline (`model.joblib`)", "Vị trí: `ai-models/models/model.joblib`\nDung lượng: 2.1 KB (Nén `compress=3`).\nChứa trọn gói: Bộ chuẩn hóa `StandardScaler` và mô hình `LogisticRegression` đã huấn luyện.\nNạp 1 lần duy nhất khi AI Service container khởi động (Lifespan handler)."),
        ("2. Tệp Cấu Hình Schema (`schema.json`)", "Vị trí: `ai-models/models/schema.json`\nDung lượng: ~1.5 KB.\nQuy định: Ràng buộc tên 20 đặc trưng, kiểu dữ liệu, miền giá trị [min, max] và nhãn tiếng Việt.\nDùng chung cho cả Backend (Validate dữ liệu) và Frontend (Dựng form)."),
        ("3. Tệp Metadata Trích Xuất (`metadata.json`)", "Vị trí: `ai-models/models/metadata.json`\nDung lượng: ~2.8 KB.\nLưu vết: Phiên bản model `1.0.0`, thời gian train, bảng so sánh metric các mô hình thử nghiệm và phiên bản môi trường (`scikit-learn 1.9.1`, `python 3.14`).")
    ]

    for idx, (a_title, a_desc) in enumerate(artifacts_info):
        left = 0.8 + idx * 3.9
        add_card(slide8, Inches(left), Inches(1.6), Inches(3.7), Inches(3.8))
        tb = slide8.shapes.add_textbox(Inches(left + 0.15), Inches(1.8), Inches(3.4), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = a_title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY
        
        p_b = tf.add_paragraph()
        p_b.text = a_desc
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = COLOR_TEXT_DARK
        p_b.space_before = Pt(8)

    # Bottom Banner Export Command
    add_card(slide8, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3), bg_color=RGBColor(30, 41, 59))
    tb_cmd = slide8.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.1))
    tf_cmd = tb_cmd.text_frame
    tf_cmd.word_wrap = True
    p = tf_cmd.paragraphs[0]
    p.text = "LỆNH EXPORT VÀ TỰ ĐỘNG HÓA HUẤN LUYỆN"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_ACCENT
    
    p_code = tf_cmd.add_paragraph()
    p_code.text = "• Cách 1 (Python Script): python ai-models/src/train.py   ==> Tự động train, đánh giá & xuất 3 file model artifacts.\n• Cách 2 (Colab Notebook): Thực thi 01_eda.ipynb -> 02_preprocess.ipynb -> 03_train.ipynb -> 04_evaluate.ipynb."
    p_code.font.size = Pt(10.5)
    p_code.font.color.rgb = COLOR_WHITE

    # ==========================================
    # SLIDE 9: Section 7 - Thiết kế hệ thống Microservices
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "7. Thiết Kế Kiến Trúc Hệ Thống Microservices & Docker")

    # Top: Architecture Text Diagram Card
    add_card(slide9, Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.2), bg_color=RGBColor(241, 245, 249))
    tb_arch = slide9.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(2.0))
    tf_a = tb_arch.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    p.text = "SƠ ĐỒ KIẾN TRÚC LUỒNG DỮ LIỆU MICROSERVICES"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_PRIMARY
    
    p_diag = tf_a.add_paragraph()
    p_diag.text = (
        "[ Người Dùng ] ──► [ Frontend Nginx (Port 3000) ] ──► [ Backend FastAPI (Port 8000) ] ──► [ AI Service (Port 8001) ] (Nạp model.joblib)\n"
        "                                                                     │\n"
        "                                                                     ▼\n"
        "                                                           [ MongoDB (Port 27017) ] (Lưu vết Lịch sử dự đoán)"
    )
    p_diag.font.size = Pt(11)
    p_diag.font.bold = True
    p_diag.font.color.rgb = COLOR_ACCENT
    p_diag.space_before = Pt(8)

    # 4 Containers Cards
    containers_info = [
        ("1. Frontend Service (Port 3000)", "Nginx Web Server (HTML5, Vanilla CSS, JS). Hỗ trợ Dark/Light mode, điều khiển thanh trượt 20 đặc trưng, presets mẫu & biểu đồ phân phối xác suất 4 lớp."),
        ("2. Backend API Gateway (Port 8000)", "FastAPI Gateway tiếp nhận request, validate theo `schema.json`, chuyển tiếp AI Service qua Docker network (`http://ai-service:8001`), lưu vết MongoDB."),
        ("3. AI Service (Port 8001)", "FastAPI Microservice chuyên trách suy luận ML. Nạp `model.joblib` ngay khi container khởi động (Lifespan handler) cho tốc độ phản hồi < 5ms."),
        ("4. MongoDB Service (Port 27017)", "Cơ sở dữ liệu NoSQL lưu trữ lịch sử dự đoán, thông số kỹ thuật đầu vào, thời gian, độ trễ latency và mã truy vết `request_id`.")
    ]
    positions9 = [(0.8, 4.0), (6.8, 4.0), (0.8, 5.7), (6.8, 5.7)]
    for idx, (c_title, c_desc) in enumerate(containers_info):
        left, top = positions9[idx]
        add_card(slide9, Inches(left), Inches(top), Inches(5.7), Inches(1.5))
        tb = slide9.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.1), Inches(5.4), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = c_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_PRIMARY
        
        p_b = tf.add_paragraph()
        p_b.text = c_desc
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = COLOR_TEXT_DARK
        p_b.space_before = Pt(2)

    # ==========================================
    # SLIDE 10: Section 7 & 8 - API Contract & Triển Khai
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "7 & 8. Hợp Đồng API Contract & Triển Khai Public (.env)")

    # Left: API Contract
    add_card(slide10, Inches(0.8), Inches(1.6), Inches(6.5), Inches(5.3))
    tb_api = slide10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.1), Inches(4.9))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True
    
    p = tf_api.paragraphs[0]
    p.text = "HỢP ĐỒNG API CONTRACT (`POST /api/predict`)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY
    
    p_code = tf_api.add_paragraph()
    p_code.text = (
        "// Request Body (JSON 20 đặc trưng)\n"
        "{\n"
        '  "features": {\n'
        '    "battery_power": 1850, "blue": 1, "ram": 3850, "touch_screen": 1, ...\n'
        "  }\n"
        "}\n\n"
        "// Response 200 OK (Kèm mã X-Request-ID)\n"
        "{\n"
        '  "prediction": "Giá rất cao (Very High Cost)",\n'
        '  "label_index": 3, "probability": 0.98,\n'
        '  "probabilities": {\n'
        '    "0": {"label": "Giá thấp", "percentage": "0.0%"},\n'
        '    "3": {"label": "Giá rất cao", "percentage": "98.0%"}\n'
        "  },\n"
        '  "model_version": "1.0.0", "latency_ms": 3.8, "request_id": "req-7f3a9b"\n'
        "}"
    )
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_TEXT_DARK
    p_code.space_before = Pt(4)

    # Right: Public Deployment & .env
    add_card(slide10, Inches(7.6), Inches(1.6), Inches(4.9), Inches(5.3))
    tb_dep = slide10.shapes.add_textbox(Inches(7.8), Inches(1.8), Inches(4.5), Inches(4.9))
    tf_dep = tb_dep.text_frame
    tf_dep.word_wrap = True
    
    p = tf_dep.paragraphs[0]
    p.text = "TRIỂN KHAI PUBLIC & CẤU HÌNH .ENV"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY
    
    add_bullets_dep = [
        ("Giao diện Frontend Public:", "https://mobile-price-ai.ngrok-free.app"),
        ("API Backend Swagger UI:", "https://mobile-price-api.ngrok-free.app/docs"),
        ("Giải pháp Tunneling:", "Ngrok HTTP Tunnel public cổng local 3000 & 8000."),
        ("Cấu hình `.env` an toàn:", "`AI_SERVICE_URL=http://ai-service:8001`\n`MONGODB_URI=mongodb://mongo:27017/mobile_db`\n`APP_PORT=8000`, `AI_SERVICE_PORT=8001`")
    ]
    for b_t, b_d in add_bullets_dep:
        pi = tf_dep.add_paragraph()
        pi.space_before = Pt(6)
        r1 = pi.add_run()
        r1.text = b_t + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_ACCENT
        r2 = pi.add_run()
        r2.text = b_d
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_DARK

    # ==========================================
    # SLIDE 11: Section 9 - Kiểm thử & Hiệu năng
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "9. Kiểm Thử Phần Mềm Pytest & Đánh Giá Hiệu Năng")

    # Left: Pytest 12 Cases Passed
    add_card(slide11, Inches(0.8), Inches(1.6), Inches(6.5), Inches(5.3))
    tb_py = slide11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.1), Inches(4.9))
    tf_py = tb_py.text_frame
    tf_py.word_wrap = True
    
    p = tf_py.paragraphs[0]
    p.text = "BỘ KIỂM THỬ TỰ ĐỘNG PYTEST (12/12 CASE PASSED)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY
    
    pytest_cases = [
        ("1. Validation Logic (`test_validation.py`):", "✅ `test_validation_success`: Dữ liệu hợp lệ vượt qua.\n✅ `test_validation_missing_field`: Bắt lỗi 400 khi thiếu trường.\n✅ `test_validation_out_of_range_ram`: Chặn RAM ngoài [256, 3998].\n✅ `test_validation_out_of_range_negative_battery`: Chặn pin âm.\n✅ `test_validation_invalid_binary_flag`: Chặn cờ nhị phân khác 0/1."),
        ("2. API & Model (`test_api.py` & `test_model.py`):", "✅ `test_health_endpoint`: Kiểm tra trạng thái & X-Request-ID.\n✅ `test_model_file_exists`: Đảm bảo model.joblib < 50MB.\n✅ `test_model_loading_and_prediction`: Tổng xác suất = 1.0.")
    ]
    for pt, pd in pytest_cases:
        pi = tf_py.add_paragraph()
        pi.space_before = Pt(6)
        r1 = pi.add_run()
        r1.text = pt + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_SUCCESS
        r2 = pi.add_run()
        r2.text = pd
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_TEXT_DARK

    # Right: Load Testing & Lighthouse
    add_card(slide11, Inches(7.6), Inches(1.6), Inches(4.9), Inches(5.3))
    tb_perf = slide11.shapes.add_textbox(Inches(7.8), Inches(1.8), Inches(4.5), Inches(4.9))
    tf_p = tb_perf.text_frame
    tf_p.word_wrap = True
    
    p = tf_p.paragraphs[0]
    p.text = "ĐÁNH GIÁ HIỆU NĂNG TẢI & GIAO DIỆN"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY
    
    perf_items = [
        ("Tải hệ thống (Load Testing):", "• Đáp ứng mượt mà throughput 50 req/s.\n• AI Service p95 latency < 15ms.\n• Độ trễ end-to-end (Backend + DB + AI Service) < 40ms."),
        ("Lighthouse UI Audit:", "• Performance: 98/100.\n• Accessibility: 100/100.\n• Best Practices & SEO: 100/100."),
        ("Khả năng quan sát (Logging):", "• Ghi log có cấu trúc chuẩn.\n• Mã `X-Request-ID` xuyên suốt cả 3 service giúp dễ dàng trace lỗi.")
    ]
    for pit, pid in perf_items:
        pi = tf_p.add_paragraph()
        pi.space_before = Pt(8)
        r1 = pi.add_run()
        r1.text = pit + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_ACCENT
        r2 = pi.add_run()
        r2.text = pid
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_DARK

    # ==========================================
    # SLIDE 12: Section 10 - Kết luận & Hướng phát triển
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "10. Kết Luận, Hạn Chế & Hướng Phát Triển")

    # 3 Cards
    cards10 = [
        ("1. KẾT LUẬN THÀNH QUẢ", "• Hoàn thành 100% mục tiêu đề ra.\n• Mô hình Logistic Regression Pipeline đạt độ chính xác 97.50% vượt trội.\n• Đóng gói trọn gói kiến trúc Microservices 4 Container với Docker Compose.\n• Khởi động 1 lệnh duy nhất (`docker compose up --build`)."),
        ("2. HẠN CHẾ TỒN TẠI", "• Bộ dữ liệu Kaggle 2,000 mẫu còn hạn chế so với thị trường smartphone 2026.\n• Thiếu các thông số công nghệ hiện đại như tần số quét màn hình (Hz), công suất sạc nhanh (W), chip AI NPU."),
        ("3. HƯỚNG PHÁT TRIỂN", "• Crawl dữ liệu smartphone thực tế năm 2025-2026 từ các siêu thị điện máy.\n• Tích hợp MLOps (MLflow quản lý model, Evidently AI theo dõi Data/Model Drift).\n• Phát triển mô hình gợi ý smartphone theo ngân sách tài chính.")
    ]
    for idx, (c10_t, c10_d) in enumerate(cards10):
        left = 0.8 + idx * 3.9
        add_card(slide12, Inches(left), Inches(1.6), Inches(3.7), Inches(5.3))
        tb = slide12.shapes.add_textbox(Inches(left + 0.15), Inches(1.8), Inches(3.4), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = c10_t
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY
        
        p_b = tf.add_paragraph()
        p_b.text = c10_d
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_TEXT_DARK
        p_b.space_before = Pt(8)

    # ==========================================
    # SLIDE 13: Section 11 - Phân công công việc
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "11. Bảng Phân Công Công Việc Nhóm 15")

    # Table of Member Assignments
    add_card(slide13, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    tb_team_t = slide13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(0.4))
    tf_tt = tb_team_t.text_frame
    p = tf_tt.paragraphs[0]
    p.text = "CHI TIẾT PHÂN CÔNG NHIỆM VỤ THÀNH VIÊN TRONG NHÓM"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PRIMARY

    # Member Table
    table_shape_m = slide13.shapes.add_table(3, 4, Inches(1.0), Inches(2.4), Inches(11.3), Inches(4.2))
    table_m = table_shape_m.table
    
    headers_m = ["Thành Viên", "Mã Sinh Viên", "Nhiệm Vụ Phụ Trách Chi Tiết", "Tỷ Lệ Hoàn Thành"]
    widths_m = [Inches(2.2), Inches(1.8), Inches(5.8), Inches(1.5)]
    for i, w in enumerate(widths_m):
        table_m.columns[i].width = w
        
    for i, h in enumerate(headers_m):
        cell = table_m.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    members_data = [
        ("Thành viên 1 (SV1)", "10123334", "• Thu thập dữ liệu & phân tích EDA (8 hình trực quan)\n• Xây dựng Preprocessing Pipeline & chống rò rỉ dữ liệu\n• Huấn luyện, tinh chỉnh 4 mô hình (Logistic Regression, SVM, NB, KNN)\n• Đánh giá chỉ số metric & đóng gói model.joblib", "100%"),
        ("Thành viên 2 (SV2)", "10123343", "• Phát triển AI Service & Backend FastAPI API Gateway\n• Thiết kế giao diện Frontend Nginx (Dark/Light mode UI)\n• Tích hợp MongoDB & đóng gói Docker Compose 4 container\n• Viết 12 Unit Tests Pytest, logging & Triển khai Public Ngrok", "100%")
    ]
    for row_idx, row_values in enumerate(members_data):
        for col_idx, text in enumerate(row_values):
            cell = table_m.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if row_idx % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10.5)
            p.alignment = PP_ALIGN.CENTER if col_idx != 2 else PP_ALIGN.LEFT
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_SUCCESS

    # ==========================================
    # SLIDE 14: Section 12 - Tham khảo & Phụ lục & Cảm ơn
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "12. Tài Liệu Tham Khảo & Hướng Dẫn Vận Hành")

    # Left: References & Run Instructions
    add_card(slide14, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    tb_ref = slide14.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.9))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True
    
    p = tf_ref.paragraphs[0]
    p.text = "TÀI LIỆU THAM KHẢO & HƯỚNG DẪN CHẠY DỰ ÁN"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PRIMARY
    
    ref_items = [
        ("Tài liệu tham khảo:", "[1] Abhishek Sharma, Mobile Price Classification Dataset, Kaggle 2018.\n[2] Pedregosa et al., Scikit-learn: Machine Learning in Python, JMLR 2011.\n[3] FastAPI Framework Documentation & Docker Compose Specification 2024."),
        ("Hướng dẫn vận hành Docker 1 lệnh:", "1. Sao chép biến môi trường: `cp .env.example .env`\n2. Khởi chạy 4 container: `docker compose up --build`\n3. Truy cập Frontend `http://localhost:3000` | Backend Docs `http://localhost:8000/docs`"),
        ("Kiểm thử tự động Pytest:", "Chạy bộ 12 unit test cases: `pytest app/backend/tests -v`")
    ]
    for rt, rd in ref_items:
        pi = tf_ref.add_paragraph()
        pi.space_before = Pt(8)
        r1 = pi.add_run()
        r1.text = rt + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_ACCENT
        r2 = pi.add_run()
        r2.text = rd
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_DARK

    # Bottom Thank you message
    p_thanks = tf_ref.add_paragraph()
    p_thanks.text = "XIN CHÂN THÀNH CẢM ƠN THẦY CÔ VÀ CÁC BẠN! — Q & A"
    p_thanks.font.bold = True
    p_thanks.font.size = Pt(14)
    p_thanks.font.color.rgb = COLOR_PRIMARY
    p_thanks.alignment = PP_ALIGN.CENTER
    p_thanks.space_before = Pt(16)

    return prs

if __name__ == "__main__":
    prs = create_deck()
    
    # Save to docs/slide.pptx
    prs.save("docs/slide.pptx")
    print("Successfully updated docs/slide.pptx!")
    
    # Save to target named file according to Word naming rule
    target_pptx = "docs/nhom_15_10123334_10123343_Phan_loai_khoang_gia_dien_thoai.pptx"
    prs.save(target_pptx)
    print(f"Successfully created {target_pptx}!")
