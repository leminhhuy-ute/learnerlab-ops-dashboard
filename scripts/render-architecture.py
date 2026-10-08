"""Generate the week 1 architecture overview as SVG and PNG, without web access."""
from pathlib import Path
from xml.sax.saxutils import escape
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1680, 1080
COLORS = {"ink": "#15304b", "muted": "#51697e", "line": "#6c8294", "blue": "#1666b0", "orange": "#b77316", "green": "#157761"}
im = Image.new("RGB", (W, H), "#f4f7fb")
draw = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<title>Kiến trúc dự kiến AWS Learner Lab Ops Dashboard</title>',
       '<desc>Nền tảng VPC/S3 tuần 1 đã triển khai AWS; pipeline kiểm kê và chi phí dự kiến tuần 2 đến 3.</desc>',
       f'<rect width="{W}" height="{H}" fill="#f4f7fb"/>']


def font(size, bold=False):
    candidates = [Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
                  Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def txt(x, y, value, size=20, bold=False, color=None):
    color = color or COLORS["ink"]
    draw.text((x, y), value, font=font(size, bold), fill=color)
    weight = ' font-weight="700"' if bold else ""
    svg.append(f'<text x="{x}" y="{y + size}" fill="{color}" font-family="Arial,DejaVu Sans,sans-serif" font-size="{size}"{weight}>{escape(value)}</text>')


def rect(x, y, w, h, fill, outline="#d5e0ea", radius=16):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=outline, width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{outline}" stroke-width="2"/>')


def box(x, y, w, h, title, lines, accent="blue"):
    rect(x, y, w, h, "#ffffff")
    color = COLORS[accent]
    draw.rounded_rectangle((x, y, x + 7, y + h), radius=3, fill=color)
    svg.append(f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3" fill="{color}"/>')
    txt(x + 22, y + 16, title, 23, True, color)
    for i, line in enumerate(lines):
        txt(x + 22, y + 54 + i * 28, line, 19, color=COLORS["muted"])


def arrow(points, label=None, label_at=None):
    color = COLORS["line"]
    draw.line(points, fill=color, width=3)
    svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="3"/>')
    a, b = points[-2:]
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    head = [b, (b[0] - 12 * math.cos(angle - .5), b[1] - 12 * math.sin(angle - .5)),
            (b[0] - 12 * math.cos(angle + .5), b[1] - 12 * math.sin(angle + .5))]
    draw.polygon(head, fill=color)
    svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in head)}" fill="{color}"/>')
    if label and label_at:
        txt(*label_at, label, 16, color=COLORS["muted"])


txt(44, 27, "AWS LEARNER LAB", 17, True, COLORS["blue"])
txt(44, 58, "Ops Dashboard — Kiến trúc dự kiến", 38, True)
txt(44, 115, "24110019 · Lê Minh Huy     |     Project: learnerlab-ops     |     Triển khai: us-east-1", 22, color=COLORS["muted"])
rect(44, 168, 1592, 38, "#e7eff8", "#e7eff8", 8)
txt(58, 173, "THIẾT KẾ TUẦN 2–3     ·     Collector dùng LabRole và môi trường Lambda mặc định", 19, True, COLORS["blue"])

# Lines first keep the arrow endpoints clear at the box borders.
arrow([(350, 300), (435, 300)], "Trigger", (365, 272))
arrow([(350, 515), (435, 515)], "Trigger", (365, 487))
arrow([(720, 300), (850, 300)], "Snapshot", (743, 272))
arrow([(720, 515), (793, 515), (793, 350), (850, 350)])
arrow([(570, 397), (570, 375)])
arrow([(570, 670), (570, 590)], "Đọc API", (587, 621))
arrow([(720, 335), (755, 335), (755, 640), (850, 640)])
arrow([(720, 550), (775, 550), (775, 676), (850, 676)])
arrow([(1250, 300), (1150, 300)], "Đọc cache", (1162, 272))
arrow([(1385, 490), (1385, 365)], "HTTPS + token", (1407, 419))
arrow([(1385, 700), (1385, 620)], "HTTPS URL tạm thời", (1407, 650))

box(44, 240, 306, 135, "EventBridge rule", ["Kiểm kê mỗi 15 phút", "Chỉ kích hoạt Lambda"])
box(44, 455, 306, 135, "EventBridge rule", ["Lấy chi phí 2 lần/ngày", "Tách lịch khỏi kiểm kê"])
box(435, 240, 285, 135, "Inventory Lambda", ["Chuẩn hóa tài nguyên", "Ghi trạng thái thiếu quyền"])
box(435, 455, 285, 135, "Billing Lambda", ["Giới hạn request/ngày", "Cache chi phí + thời điểm"])
rect(422, 397, 315, 40, "#ecf3fa", "#ecf3fa", 8)
txt(436, 402, "EC2 · RDS · SageMaker · EKS", 18, True, COLORS["blue"])
rect(422, 672, 315, 73, "#fff5e8", "#f4dec0", 8)
txt(436, 682, "Cost Explorer · dữ liệu có độ trễ", 17, True, COLORS["orange"])
txt(436, 713, "Tối đa 4 request/ngày, kể cả trang", 16, color=COLORS["muted"])
box(850, 240, 300, 135, "DynamoDB", ["LATEST + lịch sử + TTL", "API chỉ đọc dữ liệu cache"])
box(850, 590, 300, 135, "SNS", ["Cảnh báo vượt ngưỡng", "Chống lặp / cooldown"], "orange")
box(1250, 240, 386, 125, "HTTP API + Read Lambda", ["Lambda authorizer · LabRole", "CORS origin cụ thể · HTTPS"])
box(1250, 490, 386, 130, "Trình duyệt sinh viên", ["Biểu đồ + tài nguyên + chi phí", "Token phiên nhập khi demo"])
box(1250, 700, 386, 113, "S3 riêng tư", ["HTML độc lập · URL presigned", "Giữ Block Public Access"], "green")
txt(44, 780, "CloudWatch: logs, lỗi collector/API và thời điểm dữ liệu gần nhất. Giới hạn retention ở bước triển khai.", 19, color=COLORS["muted"])
txt(44, 815, "Kiểm kê hai Region: us-east-1 / us-west-2. Chi phí có độ trễ; thiếu quyền phải được hiển thị rõ.", 19, color=COLORS["muted"])

rect(44, 875, 1592, 153, "#eaf5f0", "#c8e2d7")
txt(64, 890, "NỀN TẢNG TUẦN 1 — ĐÃ TRIỂN KHAI TRÊN AWS LEARNER LAB", 22, True, COLORS["green"])
txt(64, 935, "VPC 10.20.0.0/16 · 2 subnet/hai AZ · IGW + route · Tắt auto public IPv4", 20)
txt(64, 971, "LabRole có sẵn · S3 riêng tư/SSE-S3/Retain · Tag Project=learnerlab-ops, Owner=24110019", 20)
txt(44, 1041, "Bản thiết kế cập nhật 08/10/2026 · Nền tảng thật ở docs/week-1/07-deployment-record.md", 16, color=COLORS["muted"])

svg.append("</svg>")
(OUT / "architecture.svg").write_text("\n".join(svg), encoding="utf-8")
im.save(OUT / "architecture.png")
print(f"Generated {OUT / 'architecture.svg'} and {OUT / 'architecture.png'}")
