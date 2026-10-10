"""Render the Week 1 ops-dashboard architecture in a compact monochrome style."""
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"
W, H = 2400, 1540
INK, MID, LIGHT, PALE, WHITE = "#292929", "#555555", "#eeeeee", "#f7f7f7", "#ffffff"
FONT_DIR = Path("C:/Windows/Fonts")
FONT = FONT_DIR / "arial.ttf"
FONT_BOLD = FONT_DIR / "arialbd.ttf"

im = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="#ffffff"/>']


def fnt(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def txt(x, y, s, size=30, bold=False, color=INK, anchor=None):
    d.text((x, y), s, font=fnt(size, bold), fill=color, anchor="ra" if anchor == "end" else anchor)
    lines = s.split("\n")
    svg.append(f'<text x="{x}" y="{y+size}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{"700" if bold else "400"}" text-anchor="{"end" if anchor == "end" else "middle" if anchor == "middle" else "start"}">')
    for i, line in enumerate(lines):
        svg.append(f'<tspan x="{x}" dy="{0 if i == 0 else size*1.28}">{escape(line)}</tspan>')
    svg.append("</text>")


def draw_arrow_head(a, b, color=MID):
    import math
    x1, y1 = a
    x2, y2 = b
    angle = math.atan2(y2-y1, x2-x1)
    length, spread = 20, .56
    pts = [(x2, y2), (x2-length*math.cos(angle-spread), y2-length*math.sin(angle-spread)),
           (x2-length*math.cos(angle+spread), y2-length*math.sin(angle+spread))]
    d.polygon(pts, fill=color)


def segment(a, b, color=MID, width=5, dashed=False):
    if not dashed:
        d.line((*a, *b), fill=color, width=width)
        return
    x1, y1 = a
    x2, y2 = b
    import math
    dx, dy = x2-x1, y2-y1
    length = math.hypot(dx, dy)
    if not length:
        return
    ux, uy, pos = dx/length, dy/length, 0
    while pos < length:
        end = min(pos+15, length)
        d.line((x1+ux*pos, y1+uy*pos, x1+ux*end, y1+uy*end), fill=color, width=width)
        pos = end+10


def link(points, dashed=False, color=MID, width=5, end=True, start=False):
    for a, b in zip(points, points[1:]):
        segment(a, b, color, width, dashed)
    if end:
        draw_arrow_head(points[-2], points[-1], color)
    if start:
        draw_arrow_head(points[1], points[0], color)
    pts = " ".join(f"{x},{y}" for x, y in points)
    dash = ' stroke-dasharray="15 10"' if dashed else ""
    marker_end = ' marker-end="url(#arrow)"' if end else ""
    marker_start = ' marker-start="url(#arrow)"' if start else ""
    svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="square" stroke-linejoin="round"{dash}{marker_end}{marker_start}/>')


def box(x, y, w, h, title, body, status="planned", body_size=32):
    border = INK if status == "verified" else MID
    if status == "verified":
        d.rectangle((x, y, x+w, y+h), fill=WHITE, outline=border, width=5)
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="{border}" stroke-width="5"/>')
    else:
        d.rectangle((x, y, x+w, y+h), fill=WHITE)
        for a, b in [((x,y),(x+w,y)),((x+w,y),(x+w,y+h)),((x+w,y+h),(x,y+h)),((x,y+h),(x,y))]:
            segment(a, b, border, 4, True)
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="{border}" stroke-width="4" stroke-dasharray="15 10"/>')
    hh = 62
    d.rectangle((x+2, y+2, x+w-2, y+hh), fill=LIGHT)
    d.line((x, y+hh, x+w, y+hh), fill=border, width=3)
    svg.append(f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{hh-2}" fill="{LIGHT}"/>')
    svg.append(f'<line x1="{x}" y1="{y+hh}" x2="{x+w}" y2="{y+hh}" stroke="{border}" stroke-width="3"/>')
    txt(x+18, y+10, title, size=34, bold=True)
    txt(x+18, y+hh+16, body, size=body_size, color=MID)


def label(x, y, text, size=25, color=MID, bold=False):
    ft = fnt(size, bold)
    b = d.textbbox((x, y), text, font=ft)
    d.rectangle((b[0]-7, b[1]-3, b[2]+7, b[3]+4), fill=WHITE)
    d.text((x, y), text, font=ft, fill=color)
    svg.append(f'<rect x="{b[0]-7}" y="{b[1]-3}" width="{b[2]-b[0]+14}" height="{b[3]-b[1]+7}" fill="#ffffff"/>')
    txt(x, y, text, size=size, bold=bold, color=color)


# Title and key.
txt(70, 34, "KIẾN TRÚC TỔNG THỂ — OPS DASHBOARD AWS LEARNER LAB", size=48, bold=True)
txt(72, 104, "Thu thập tài nguyên và chi phí → lưu snapshot → API đọc dữ liệu → giao diện, cảnh báo và giám sát", size=31, color=MID)
d.line((70, 170, 2320, 170), fill=INK, width=3)
svg.append('<line x1="70" y1="170" x2="2320" y2="170" stroke="#292929" stroke-width="3"/>')
d.rectangle((76, 194, 122, 236), fill=WHITE, outline=INK, width=4)
svg.append('<rect x="76" y="194" width="46" height="42" fill="#ffffff" stroke="#292929" stroke-width="4"/>')
txt(140, 194, "Tài nguyên đã xác minh tuần 1", size=27, color=MID)
segment((650,215),(710,215),MID,4,True)
svg.append('<line x1="650" y1="215" x2="710" y2="215" stroke="#555555" stroke-width="4" stroke-dasharray="15 10"/>')
txt(730, 194, "Dịch vụ / luồng dự kiến tuần 2–3", size=27, color=MID)
txt(2300, 194, "Mũi tên liền: luồng dữ liệu; hai đầu = request / response", size=25, color=MID, anchor="end")

# One AWS boundary; the browser stays outside it.
d.rectangle((70, 265, 2140, 990), fill=WHITE, outline=MID, width=4)
svg.append('<rect x="70" y="265" width="2070" height="725" fill="none" stroke="#555555" stroke-width="4"/>')
d.rectangle((95, 245, 925, 287), fill=WHITE)
txt(105, 240, "AWS LEARNER LAB  ·  213858341631  ·  us-east-1", size=28, bold=True, color=MID)

# The main operational flow is laid out on one line so the services read as one system.
box(120, 395, 340, 210, "EventBridge", "Inventory: mỗi 15 phút\nBilling: 2 lần/ngày UTC", body_size=26)
box(590, 395, 420, 210, "Lambda collectors", "Kiểm kê: EC2/EBS/RDS\nSageMaker/EKS · 2 Region\nCost Explorer API\n≤ 4 request/ngày UTC", body_size=24)
box(1120, 395, 340, 210, "DynamoDB", "Inventory / billing cache\nTrạng thái nguồn\nThời gian thu thập UTC", body_size=25)
box(1510, 395, 290, 210, "Lambda API", "Read snapshot\nKhông gọi CE", body_size=26)
box(1850, 395, 260, 210, "API Gateway", "HTTP API\nHTTPS GET", body_size=28)

link([(460,490),(590,490)])
link([(1010,465),(1120,465)])
link([(1850,490),(1800,490)], start=True)
link([(1510,530),(1460,530)], start=True)

# Student browser outside the Learner Lab account.
txt(2190, 425, "Sinh viên", size=32, bold=True)
txt(2190, 475, "Trình duyệt", size=29, color=MID)
link([(2190,530),(2110,530)], start=True)

# Alert and monitoring branches stay below the main flow.
box(590, 735, 340, 130, "SNS", "Cảnh báo vượt ngưỡng", body_size=25)
box(1010, 735, 320, 130, "Email", "Cần xác nhận subscription", body_size=23)
box(1390, 735, 340, 130, "CloudWatch", "Logs và metrics", body_size=25)
link([(760,605),(760,735)])
link([(930,800),(1010,800)])
link([(860,605),(860,675),(1560,675),(1560,735)], dashed=True)
link([(1655,605),(1655,735)], dashed=True)

# Week 1's private bucket is real; only the planned frontend object and access path are dashed.
box(1850, 635, 260, 125, "Authorizer", "Bearer · Allow / Deny", body_size=22)
box(1850, 800, 260, 160, "Amazon S3", "Đã tạo tuần 1\nPrivate · SSE-S3\nHTML chưa upload", status="verified", body_size=20)
link([(2110,845),(2145,845),(2145,555),(2190,555)], dashed=True, start=True)
link([(1980,605),(1980,635)], dashed=True)

# Deployed foundation, with the S3 bucket shown once in its actual data path above.
txt(70, 1035, "NỀN TẢNG TUẦN 1 — ĐÃ TRIỂN KHAI VÀ KIỂM TRA", size=33, bold=True)
d.rectangle((70, 1090, 2320, 1495), fill=PALE, outline=INK, width=4)
d.line((1195,1090,1195,1495), fill=MID, width=3)
svg.extend(['<rect x="70" y="1090" width="2250" height="405" fill="#f7f7f7" stroke="#292929" stroke-width="4"/>',
            '<line x1="1195" y1="1090" x2="1195" y2="1495" stroke="#555555" stroke-width="3"/>'])
txt(110, 1130, "VPC · 10.20.0.0/16", size=37, bold=True)
txt(110, 1205, "2 subnet /24 · IGW và route Internet", size=32, color=MID)
txt(110, 1262, "Không tạo EC2, NAT Gateway hoặc EIP", size=30, color=MID)
txt(110, 1318, "VPC là nền tảng lab, không nằm trên luồng serverless dự kiến", size=28, color=MID)
txt(1240, 1130, "Tag và quyền trong Learner Lab", size=37, bold=True)
txt(1240, 1205, "S3: Block Public Access · SSE-S3", size=30, color=MID)
txt(1240, 1262, "Tag: Project=learnerlab-ops · Owner=24110019", size=29, color=MID)
txt(1240, 1318, "LabRole có sẵn; không tạo IAM role mới", size=29, color=MID)
txt(1240, 1374, "Quyền pipeline cần kiểm tra trước khi triển khai", size=28, color=MID)

svg.insert(1, '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#555555"/></marker></defs>')
svg.append("</svg>")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "architecture-week1-simple.svg").write_text("\n".join(svg), encoding="utf-8")
im.resize((1800, 1155), Image.Resampling.LANCZOS).save(OUT / "architecture-week1-simple.png", dpi=(96, 96))
print(f"Wrote {OUT / 'architecture-week1-simple.png'} and {OUT / 'architecture-week1-simple.svg'}")
