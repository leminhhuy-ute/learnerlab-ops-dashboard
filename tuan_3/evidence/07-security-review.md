# Rà soát cấu hình bảo mật S3 và API — 20/10/2026

Đối chiếu trực tiếp trong AWS Console, Account `213858341631`, Region `us-east-1`. Chỉ đọc cấu hình, không sửa quyền hay chính sách.

| Thành phần | Cấu hình nhìn thấy trên Console | Kết quả |
|---|---|---|
| S3 `learnerlab-ops-week2-dashboard-213858341631` | `Block all public access: On`; cả bốn lựa chọn Block Public Access đều bật | Đạt kiểm tra chặn truy cập công khai |
| S3 — mã hóa mặc định | Server-side encryption with Amazon S3 managed keys (`SSE-S3`) | Đạt cấu hình mã hóa yêu cầu |
| S3 — tag | `Project=learnerlab-ops`, `Owner=24110019`, `Environment=learner-lab` | Có tag nhận diện dự án/chủ sở hữu |
| API Gateway `learnerlab-ops-week2-api`, route `GET /summary` | Authorization: `IAM (built-in)` | Route vẫn yêu cầu xác thực IAM; không chuyển sang public |

## Giới hạn của lần kiểm tra

CloudShell trong cùng phiên trả explicit deny từ `voc-cancel-cred` cho một số lệnh chỉ đọc; vì vậy bảng này chỉ ghi những thuộc tính hiển thị được trên hai trang S3 và API Gateway. Chưa rà soát đầy đủ quyền thực thi của `LabRole`, các route khác, cấu hình log/API hoặc toàn bộ đường đi dữ liệu. Đây là một phần của mục bảo mật tuần 3, không phải tuyên bố đã hoàn tất toàn bộ kiểm toán.

