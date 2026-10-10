from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "Bao_cao_tuan_1_Learner_Lab_Ops_Dashboard_24110019.docx"

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def borders(cell, color="D9D9D9"):
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.first_child_found_in("w:tcBorders")
    if b is None:
        b = OxmlElement("w:tcBorders")
        tcPr.append(b)
    for edge in ("top", "left", "bottom", "right"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), "4")
        node.set(qn("w:color"), color)
        b.append(node)

def set_cell_text(cell, value, bold=False, size=9.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(value))
    r.bold = bold
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    t.autofit = False
    for i, value in enumerate(headers):
        c = t.rows[0].cells[i]
        set_cell_text(c, value, True)
        shade(c, "ECECEC")
        borders(c)
        if widths: c.width = Cm(widths[i])
    for ri, vals in enumerate(rows):
        cells = t.add_row().cells
        for i, value in enumerate(vals):
            set_cell_text(cells[i], value)
            borders(cells[i])
            if widths: cells[i].width = Cm(widths[i])
            if ri % 2: shade(cells[i], "F8F8F8")
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t

def para(text="", style=None, bold_prefix=None):
    p = doc.add_paragraph(style=style)
    if bold_prefix and text.startswith(bold_prefix):
        p.add_run(bold_prefix).bold = True
        p.add_run(text[len(bold_prefix):])
    else:
        p.add_run(text)
    return p

def heading(text, level=1):
    doc.add_heading(text, level=level)

def caption(text):
    p = doc.add_paragraph(style="Caption")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(text)

def picture(path, width_cm, label):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    caption(label)

def set_page_border(section):
    sectPr = section._sectPr
    pgBorders = OxmlElement("w:pgBorders")
    pgBorders.set(qn("w:offsetFrom"), "page")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "8")
        e.set(qn("w:space"), "24")
        e.set(qn("w:color"), "333333")
        pgBorders.append(e)
    sectPr.append(pgBorders)

def page_number(paragraph):
    paragraph.add_run("Trang ")
    r = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r._r.addnext(fld)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin = Cm(2.3)
sec.bottom_margin = Cm(2.0)
sec.left_margin = sec.right_margin = Cm(2.35)
set_page_border(sec)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(11)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.line_spacing = 1.22
normal.paragraph_format.space_after = Pt(6)
for st_name, size in (("Title", 18), ("Heading 1", 14), ("Heading 2", 12)):
    st = styles[st_name]
    st.font.name = "Times New Roman"
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.space_before = Pt(13 if st_name != "Title" else 0)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.keep_with_next = True
title_ppr = styles["Title"]._element.get_or_add_pPr()
for title_border in title_ppr.findall(qn("w:pBdr")):
    title_ppr.remove(title_border)
styles["Caption"].font.name = "Times New Roman"
styles["Caption"].font.size = Pt(9)
styles["Caption"].font.italic = True
styles["Caption"].font.color.rgb = RGBColor(0, 0, 0)

# Trang bìa lấy nhịp bố cục từ báo cáo tham khảo, chỉ dùng dữ kiện của đề tài này.
for text, size, space in [
    ("MÔN HỌC ĐIỆN TOÁN ĐÁM MÂY", 15, 6),
    ("CLOUD - ĐỢT 1 - 2026–2027", 11, 44),
    ("BÁO CÁO TIẾN ĐỘ TUẦN 1", 18, 12),
    ("BẢNG ĐIỀU KHIỂN VẬN HÀNH", 17, 3),
    ("CHO AWS LEARNER LAB", 17, 42),
]:
    p = doc.add_paragraph()
    if text in ("BẢNG ĐIỀU KHIỂN VẬN HÀNH", "CHO AWS LEARNER LAB"):
        p.style = styles["Title"]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)

cover = doc.add_table(rows=4, cols=1)
cover.autofit = False
cover.alignment = WD_TABLE_ALIGNMENT.CENTER
for c, text in zip([r.cells[0] for r in cover.rows], [
    "Nhóm lĩnh vực: Monitoring & Operations",
    "Giảng viên hướng dẫn: Huỳnh Xuân Phụng",
    "Sinh viên: Lê Minh Huy — MSSV 24110019",
    "Minh chứng Learner Lab: 07–08/10/2026; báo cáo lập ngày 10/10/2026",
]):
    set_cell_text(c, text, size=10.5)
    borders(c, "666666")
doc.add_paragraph("\n\n\n")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Ngày 10 tháng 10 năm 2026")
r.italic = True
r.font.size = Pt(11)

bodysec = doc.add_section(WD_SECTION.NEW_PAGE)
bodysec.page_width, bodysec.page_height = Cm(21), Cm(29.7)
bodysec.top_margin = Cm(2.1)
bodysec.bottom_margin = Cm(2.0)
bodysec.left_margin = bodysec.right_margin = Cm(2.3)
for inherited_border in bodysec._sectPr.findall(qn("w:pgBorders")):
    bodysec._sectPr.remove(inherited_border)
bodysec.footer.is_linked_to_previous = False
fp = bodysec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
page_number(fp)

heading("TÓM TẮT", 1)
para("Báo cáo ghi nhận kết quả tuần 1 của đề tài Bảng điều khiển vận hành cho AWS Learner Lab. Phạm vi tuần này gồm tìm hiểu dịch vụ, chốt yêu cầu, thiết kế kiến trúc và sơ đồ, dựng nền tảng VPC/IAM LabRole/S3, gắn tag và lưu minh chứng. Các chức năng thu thập tự động, API, biểu đồ và cảnh báo thuộc kế hoạch các tuần tiếp theo; báo cáo không coi chúng là kết quả đã chạy.")
para("Trên tài khoản Learner Lab 213858341631 tại us-east-1, stack CloudFormation learnerlab-ops-week1 đạt CREATE_COMPLETE ngày 08/10/2026. Kiểm tra sau triển khai ghi nhận 10/10 tài nguyên của stack ở trạng thái CREATE_COMPLETE, gồm VPC 10.20.0.0/16, hai subnet thuộc hai Availability Zone, tuyến tới Internet Gateway và một bucket S3 riêng tư có SSE-S3. LabRole có sẵn đã được xác minh bằng IAM GetRole; LabInstanceProfile chưa được xác minh độc lập.")
para("Sinh viên Lê Minh Huy cung cấp tổng thời gian tự học/làm việc 8 giờ trong tuần 1, nhưng chưa cung cấp ngày và giờ theo từng nhiệm vụ. Codex hỗ trợ soạn thiết kế, template, thao tác triển khai và xác minh trong Learner Lab. Báo cáo giữ tách biệt số giờ sinh viên tự khai với thời gian công cụ thực hiện.")

heading("Chương 1 Tổng quan và phạm vi tuần 1", 1)
heading("1.1 Bài toán và đầu ra", 2)
para("Mục tiêu toàn dự án là hiển thị tài nguyên đang chạy, chi phí ước tính/billing đã ghi nhận và cảnh báo giúp sinh viên quản lý ngân sách Learner Lab. Sản phẩm cuối dự kiến dùng Lambda đọc metadata EC2, RDS, SageMaker và EKS; DynamoDB lưu snapshot; API và web đọc dữ liệu; SNS gửi cảnh báo. Tuần 1 chỉ chuẩn bị nền tảng và kiến trúc cho các chức năng đó.")
table(["Đầu việc tuần 1", "Sản phẩm hiện có", "Trạng thái"], [
    ("Tìm hiểu dịch vụ và giới hạn Lab", "docs/week-1/01-services-and-requirements.md", "Tài liệu đã soạn"),
    ("Thiết kế kiến trúc, sơ đồ", "docs/week-1/02-architecture.md; docs/diagrams/architecture-week1-simple.png", "Bản thiết kế"),
    ("Dựng VPC, dùng LabRole, tạo S3", "infra/week1-foundation.yaml; stack AWS", "Đã xác minh 08/10"),
    ("Gắn Project/Owner, lưu ảnh", "evidence/week-1/02–04", "Đã xác minh 08/10"),
    ("Nhật ký theo người và số giờ", "docs/week-1/worklog.csv", "Tổng 8 giờ tự khai; thiếu phân bổ"),
], [4.1, 8.2, 4.0])
caption("Bảng 1.1. Phạm vi tuần 1 và sản phẩm có thể đối chiếu")

heading("1.2 Dịch vụ đã tìm hiểu", 2)
table(["Dịch vụ", "Vai trò trong kiến trúc", "Tình trạng tuần 1"], [
    ("VPC, IAM LabRole, S3", "Nền tảng mạng/quyền, lưu artifact", "VPC và S3 đã triển khai; LabRole đã kiểm tra"),
    ("Lambda, EventBridge", "Thu thập metadata và lập lịch", "Thiết kế, chưa triển khai"),
    ("DynamoDB, API Gateway", "Lưu snapshot và cấp dữ liệu JSON", "Thiết kế, chưa triển khai"),
    ("Cost Explorer, SNS", "Đọc billing có độ trễ và cảnh báo", "Thiết kế, chưa gọi CE/chưa gửi SNS"),
    ("CloudWatch", "Theo dõi lỗi và log của các Lambda", "Thiết kế cho tuần sau"),
], [3.7, 7.6, 5.0])
caption("Bảng 1.2. Phân biệt dịch vụ đã triển khai với dịch vụ mới ở bản thiết kế")

heading("Chương 2 Thiết kế kiến trúc", 1)
heading("2.1 Luồng dự kiến", 2)
para("Hai lịch EventBridge dự kiến tách tác vụ kiểm kê và billing. Lambda kiểm kê đọc metadata tài nguyên tại us-east-1 và us-west-2; Lambda billing giới hạn số request Cost Explorer rồi ghi snapshot vào DynamoDB. API chỉ đọc snapshot để giao diện không gọi Cost Explorer mỗi lần người dùng mở trang. Khi vượt ngưỡng, nhánh SNS gửi cảnh báo. S3 giữ trang tĩnh và artifact ở chế độ riêng tư. Đây là quyết định thiết kế, chưa phải pipeline hoạt động trong tuần 1.")
picture(ROOT / "docs" / "diagrams" / "architecture-week1-simple.png", 16.1,
        "Hình 2.1. Sơ đồ đơn sắc; vùng trên đã kiểm chứng, vùng dưới là luồng dự kiến")
heading("2.2 Ranh giới đã triển khai", 2)
para("Stack tuần 1 tạo VPC và bucket làm nền tảng. Hai subnet có route 0.0.0.0/0 đến Internet Gateway nhưng MapPublicIpOnLaunch=False; việc có public route không tự cấp public IPv4. Stack không tạo EC2, NAT Gateway, Elastic IP, RDS, EKS, SageMaker, Lambda, DynamoDB hay SNS. Vai trò LabRole là tài nguyên có sẵn của Learner Lab và không do template tạo mới.")

doc.add_page_break()
heading("Chương 3 Triển khai thật trên AWS Learner Lab", 1)
heading("3.1 Tài khoản, thời điểm và CloudFormation", 2)
para("Phiên Lab được xác minh Ready ngày 07/10/2026. Trước khi triển khai ngày 08/10/2026, lệnh sts get-caller-identity xác nhận đúng tài khoản 213858341631. CloudFormation ValidateTemplate chấp nhận template; stack learnerlab-ops-week1 đạt CREATE_COMPLETE lúc 12:52:18 giờ Việt Nam. ListStackResources trả 10 tài nguyên, tất cả CREATE_COMPLETE. SHA-256 của template dùng khi triển khai là 649857a229327af489b40bd6998f35cf015fa91176026542e1610ef4e41d9bc4.")
table(["Thành phần", "Giá trị đã đọc lại từ AWS"], [
    ("Account / Region", "213858341631 / us-east-1"),
    ("VPC", "vpc-0206a78d96a4b3a57; CIDR 10.20.0.0/16"),
    ("Subnet A", "subnet-0fe1f68d4d015130c; us-east-1a; 10.20.1.0/24"),
    ("Subnet B", "subnet-0a26fc106be139906; us-east-1b; 10.20.2.0/24"),
    ("Route table / IGW", "rtb-0d686db1acc56489d / igw-0998040b443aaa624"),
    ("S3 bucket", "learnerlab-ops-week1-artifactbucket-u4t7cql7ngfo"),
    ("IAM role có sẵn", "arn:aws:iam::213858341631:role/LabRole"),
], [4.3, 12.0])
caption("Bảng 3.1. Định danh tài nguyên thật tại mốc xác minh 08/10/2026")

heading("3.2 Cấu hình bảo mật và tag", 2)
para("S3 bật đủ bốn cờ Block Public Access, mã hóa mặc định SSE-S3 AES256 và Object Ownership BucketOwnerEnforced. Bucket có quy tắc hủy multipart upload chưa hoàn tất sau 7 ngày. Các tài nguyên có hỗ trợ tag được xác minh với Project=learnerlab-ops, Owner=24110019 và Environment=learner-lab. S3 dùng DeletionPolicy: Retain, vì vậy xóa stack sau này chưa đủ để xóa bucket.")
para("GetRole xác nhận LabRole tồn tại. Template chỉ xuất chuỗi LabInstanceProfileName để tham khảo; chưa có lệnh IAM xác minh profile này. Không tạo IAM user/role mới, đúng ràng buộc Learner Lab của đề bài.")

heading("Chương 4 Minh chứng, chi phí và giới hạn", 1)
heading("4.1 Bảng đối chiếu minh chứng", 2)
table(["Ảnh", "Điều được ảnh và biên bản xác nhận"], [
    ("01-lab-session-ready.jpg", "Lab Ready, Account ID và Region ngày 07/10; chưa phải ảnh triển khai"),
    ("02-stack-complete.jpg", "Stack CREATE_COMPLETE, 10 tài nguyên, VPC/subnet/bucket ngày 08/10"),
    ("03-network-check.jpg", "VPC, hai subnet/hai AZ, auto public IPv4 tắt, route tới IGW"),
    ("04-s3-private.jpg", "Bốn cờ Block Public Access, AES256, ownership và tag"),
], [5.1, 11.2])
caption("Bảng 4.1. Minh chứng CLI có Account ID, Region và thời gian")
para("Các ảnh ngày 08/10 ghi giờ UTC−07:00; cộng 14 giờ để đổi sang giờ Việt Nam. Ảnh và repository không chứa AWS access key, secret key hoặc session token. Tệp credentials CLI tạm thời trong terminal của Lab đã được xóa sau kiểm tra; phiên Lab đã End Lab và chuyển Terminated khoảng 13:00 giờ Việt Nam.")

heading("4.2 Chi phí và mức độ quan sát", 2)
para("Cổng Learner Lab hiển thị Used $0 of $50 tại mốc quan sát được ghi trong biên bản. Đây là số hiển thị của portal có thể có độ trễ, không phải kết luận tổng chi phí thực tế bằng 0. Trong lần kiểm tra ở hai Region được phép, không thấy EC2 running hoặc NAT Gateway available. Stack tuần 1 không tạo compute hay NAT. Báo cáo chưa có số liệu Cost Explorer vì API đó chưa được dùng trong tuần 1; không điền các biểu đồ chi phí giả.")
para("Bucket S3 được giữ lại cho tuần 2; request và lưu trữ phát sinh sau mốc kiểm tra vẫn có thể tạo chi phí. Việc End Lab không tự xóa mọi tài nguyên. Cần kiểm tra lại tài nguyên và số dư khi mở Lab ở buổi sau.")

heading("Chương 5 Tiến độ, AI hỗ trợ và việc tiếp theo", 1)
heading("5.1 Nhật ký công việc", 2)
table(["Sinh viên", "Thông tin thời gian có thể xác nhận", "Thiếu để hoàn tất worklog"], [
    ("Lê Minh Huy\n24110019", "Tổng 8 giờ tuần 1 do sinh viên tự khai", "Chưa có ngày/giờ thực tế cho từng nhiệm vụ; chưa xác minh mức tự thực hiện từng phần"),
], [3.5, 5.5, 7.3])
caption("Bảng 5.1. Thời gian chỉ ghi theo mức độ thông tin đã được cung cấp")
para("Sinh viên liệt kê phạm vi 8 giờ gồm tìm hiểu dịch vụ, thiết kế kiến trúc, vẽ sơ đồ, dựng nền tảng VPC/IAM LabRole/S3 và gắn tag. Kế hoạch chia thành bốn dòng, mỗi dòng 2 giờ dự kiến; đó không phải số giờ thực tế. Worklog giữ trống giờ thực tế theo nhiệm vụ đến khi sinh viên cung cấp ngày, thời lượng và mức tham gia từng việc. Không cộng thời gian Codex thao tác vào 8 giờ của sinh viên.")
heading("5.2 Phần được AI hỗ trợ", 2)
para("Codex hỗ trợ tổng hợp yêu cầu và tài liệu AWS, thiết kế kiến trúc, vẽ sơ đồ, soạn CloudFormation/template/script, triển khai và kiểm tra nền tảng trên Learner Lab, lưu ảnh minh chứng, rồi biên soạn báo cáo này. Sinh viên phải tự đọc, kiểm tra và giải thích được cấu hình/mã nguồn khi vấn đáp. Báo cáo không gán các thao tác của Codex thành công việc trực tiếp của sinh viên.")
heading("5.3 Kết luận và tuần 2", 2)
para("Tuần 1 có đầu ra thật: tài liệu yêu cầu, sơ đồ kiến trúc, stack VPC/S3 hoàn thành, LabRole đã xác minh, tag Project/Owner/Environment và ảnh AWS có thời gian/tài khoản/vùng. Phần còn mở là phân bổ worklog theo từng đầu việc và kiểm tra LabInstanceProfile nếu cần dùng ở giai đoạn sau. Tuần 2 mới triển khai Lambda, EventBridge, DynamoDB, API và các chức năng lõi; quyền và dữ liệu của các dịch vụ này phải được kiểm tra trực tiếp trên Lab trước khi báo là hoàn tất.")
heading("Nguồn và tệp kèm theo", 1)
para("Nguồn dữ kiện AWS: docs/week-1/07-deployment-record.md; docs/week-1/04-evidence-and-review.md; evidence/week-1/01–04. Nguồn kiến trúc: docs/week-1/01-services-and-requirements.md; docs/week-1/02-architecture.md; docs/diagrams/architecture-week1-simple.png. Mã hạ tầng: infra/week1-foundation.yaml. Repository: https://github.com/leminhhuy-ute/learnerlab-ops-dashboard (riêng tư; giảng viên cần quyền truy cập).")

heading("Phụ lục Ảnh minh chứng AWS", 1)
picture(ROOT / "evidence" / "week-1" / "02-stack-complete.jpg", 14.2,
        "Phụ lục A. Stack CREATE_COMPLETE, Account 213858341631, us-east-1")
picture(ROOT / "evidence" / "week-1" / "03-network-check.jpg", 14.2,
        "Phụ lục B. VPC, subnet và tuyến Internet Gateway")
picture(ROOT / "evidence" / "week-1" / "04-s3-private.jpg", 14.2,
        "Phụ lục C. Bảo mật bucket S3 và tag Project/Owner")

doc.core_properties.title = "Báo cáo tiến độ tuần 1 Bảng điều khiển vận hành cho AWS Learner Lab"
doc.core_properties.author = "Lê Minh Huy"
doc.core_properties.subject = "Báo cáo tuần 1 đề tài Monitoring & Operations"
OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(OUT)
