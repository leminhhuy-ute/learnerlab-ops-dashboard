"""Render a restrained grayscale architecture overview for week 1."""
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1680, 900
WHITE, INK, MUTED, LINE, PALE = "#FFFFFF", "#202020", "#555555", "#707070", "#F3F3F3"
im = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<title>Kiến trúc tuần 1 của Ops Dashboard Learner Lab</title>',
       '<desc>Sơ đồ đen trắng tách tài nguyên đã xác minh tuần 1 khỏi luồng dự kiến tuần 2 đến 3.</desc>',
       f'<rect width="{W}" height="{H}" fill="{WHITE}"/>']

def font(size, bold=False):
    choices = [
        Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for p in choices:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def text(x, y, value, size=24, bold=False, color=INK):
    draw.text((x, y), value, font=font(size, bold), fill=color)
    weight = ' font-weight="700"' if bold else ""
    svg.append(f'<text x="{x}" y="{y+size}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}"{weight}>{escape(value)}</text>')

def rect(x, y, w, h, fill=WHITE, stroke=LINE, width=2):
    draw.rectangle((x, y, x+w, y+h), fill=fill, outline=stroke, width=width)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

def box(x, y, w, h, title, lines):
    rect(x, y, w, h)
    text(x+22, y+18, title, 27, True)
    for i, line in enumerate(lines):
        text(x+22, y+61+i*33, line, 22, False, MUTED)

def arrow(x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=INK, width=3)
    tip = [(x2,y2), (x2-13,y2-7), (x2-13,y2+7)]
    draw.polygon(tip, fill=INK)
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="3"/>')
    svg.append(f'<polygon points="{x2},{y2} {x2-13},{y2-7} {x2-13},{y2+7}" fill="{INK}"/>')

text(50, 35, "Ops Dashboard cho AWS Learner Lab", 39, True)
text(50, 91, "Bản thiết kế tuần 1  |  Lê Minh Huy - 24110019  |  Account 213858341631", 22, False, MUTED)

rect(45, 145, 1590, 277, PALE, "#C8C8C8")
text(68, 166, "TUẦN 1 - ĐÃ XÁC MINH TRÊN LEARNER LAB (us-east-1)", 26, True)
box(70, 225, 430, 143, "CloudFormation", ["Stack CREATE_COMPLETE", "10/10 tài nguyên hoàn thành"])
box(625, 225, 430, 143, "VPC", ["10.20.0.0/16; 2 subnet", "IGW + route; không auto public IP"])
box(1180, 225, 430, 143, "S3 riêng tư", ["Block Public Access; SSE-S3", "Project/Owner/Environment tags"])
text(70, 385, "IAM LabRole đã được xác minh; LabInstanceProfile chưa được xác minh độc lập.", 21)

rect(45, 460, 1590, 340, WHITE, "#C8C8C8")
text(68, 482, "TUẦN 2-3 - LUỒNG DỰ KIẾN, CHƯA TRIỂN KHAI", 26, True)
box(70, 560, 330, 139, "EventBridge", ["Lịch kiểm kê", "Lịch đọc chi phí"])
box(470, 560, 330, 139, "Lambda", ["EC2/RDS/SM/EKS", "Cost Explorer API"])
box(870, 560, 330, 139, "DynamoDB", ["Snapshot + thời điểm", "Trạng thái nguồn"])
box(1270, 560, 340, 139, "API + web S3", ["Đọc snapshot", "Hiển thị biểu đồ"])
arrow(400, 629, 470, 629)
arrow(800, 629, 870, 629)
arrow(1200, 629, 1270, 629)
text(70, 735, "SNS: cảnh báo vượt ngưỡng. CloudWatch: log và lỗi. Frontend không gọi Cost Explorer trực tiếp.", 22)

text(50, 838, "Mũi tên ở vùng dưới là luồng dự kiến; các khối vùng trên là kết quả AWS đã kiểm chứng.", 21, False, MUTED)
svg.append("</svg>")
(OUT / "architecture-week1-simple.svg").write_text("\n".join(svg), encoding="utf-8")
im.save(OUT / "architecture-week1-simple.png")
print(f"Generated {OUT / 'architecture-week1-simple.svg'} and {OUT / 'architecture-week1-simple.png'}")
