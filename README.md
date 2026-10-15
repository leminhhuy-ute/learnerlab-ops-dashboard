# Bảng điều khiển vận hành AWS Learner Lab

**Mã học phần:** CLCO332779 · **Sinh viên:** Lê Minh Huy — MSSV 24110019 · **Repository:** [leminhhuy-ute/learnerlab-ops-dashboard](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard)

Trang này dẫn đến hồ sơ từng tuần, kết quả AWS đã xác minh và nguồn dữ liệu. Báo cáo Word được nộp riêng qua hệ thống môn học.

| Tuần | Nội dung | Hồ sơ |
|---|---|---|
| **Tuần 1** | Tìm hiểu dịch vụ, xác định nguồn dữ liệu, thiết kế kiến trúc và dựng VPC/S3 nền tảng | [Mở hồ sơ Tuần 1](docs/week-1/README.md) · [Nguồn dữ liệu](docs/data-sources.md) |
| **Tuần 2** | Triển khai và kiểm thử các chức năng lõi trên AWS | [Mở hồ sơ Tuần 2](docs/week-2/README.md) · [Mã nguồn](src/week-2/README.md) · [Worklog](docs/week-2/worklog.csv) |

## Kết quả đã xác minh

- **Tuần 1:** CloudFormation stack `learnerlab-ops-week1` đạt `CREATE_COMPLETE` với 10 tài nguyên nền tảng tại `us-east-1`. VPC, subnet, route Internet, `LabRole` có sẵn và bucket S3 riêng tư đã được kiểm tra. Xem [biên bản triển khai](docs/week-1/07-deployment-record.md) và [ảnh nền tảng](evidence/week-1/README.md).
- **Tuần 2:** Lambda kiểm kê, billing, read API và threshold alert; DynamoDB, API Gateway, S3, EventBridge, Cost Explorer và SNS đã được triển khai/kiểm thử. Ảnh ngày 15/10/2026 ghi nhận 10 tổ hợp dịch vụ/vùng có `status=ok`, `count=0`; GET /summary có SigV4 trả HTTP 200, không ký trả HTTP 403. Giao diện hiển thị JSON thật đã nạp thủ công. Chi phí `1E-10 USD` là ước tính, không phải hóa đơn cuối kỳ.

## Nguồn dữ liệu và giới hạn

Collector đọc các API AWS cho EC2, RDS, SageMaker và EKS ở `us-east-1` và `us-west-2`; billing lấy từ AWS Cost Explorer. DynamoDB lưu snapshot, không phải nguồn dữ liệu gốc. Bảng API, phạm vi đã kiểm tra và cách diễn giải số liệu nằm ở [docs/data-sources.md](docs/data-sources.md).

Hệ thống dùng `LabRole` có sẵn, API giữ xác thực `AWS_IAM`, bucket giao diện giữ riêng tư. Vì vậy giao diện ở tuần 2 được nạp JSON đã xác thực theo cách thủ công; tự động kết nối giao diện và API được để sang giai đoạn sau.

Worklog phân biệt phần sinh viên xác nhận với phần LLM/AI (ChatGPT) hỗ trợ. Giờ chưa có xác nhận được để trống; thời gian phiên Lab, lệnh AI và mốc CloudTrail không được dùng để suy ra giờ học.

Không đưa access key, secret key, session token, URL presigned hoặc thông tin đăng nhập vào repository. Ảnh SNS công khai không hiển thị địa chỉ email người nhận.
