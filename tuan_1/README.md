# Tuần 1 — Khảo sát, thiết kế và dựng nền tảng

Tuần 1 hoàn thành việc tìm hiểu dịch vụ, chốt phạm vi dữ liệu, thiết kế kiến trúc, vẽ sơ đồ và triển khai nền tảng kiểm thử trên AWS Learner Lab.

## Kết quả trên AWS

Ngày 08/10/2026, CloudFormation stack `learnerlab-ops-week1` đạt `CREATE_COMPLETE` tại `us-east-1` với 10 tài nguyên. VPC `10.20.0.0/16`, hai subnet `/24`, Internet Gateway và route table được kiểm tra. Bucket S3 bật đủ Block Public Access, mã hóa SSE-S3 và có tag `Project=learnerlab-ops`, `Owner=24110019`. Nhóm dùng `LabRole` có sẵn, không tạo IAM user/role mới.

Tuần 1 **chưa triển khai** Lambda kiểm kê, Cost Explorer, DynamoDB, API Gateway, EventBridge hay SNS. Đó là phần kiến trúc dự kiến và được kiểm tra/triển khai ở tuần 2. Xem [bảng nguồn dữ liệu](../docs/data-sources.md).

## Tài liệu và minh chứng

- [Kế hoạch và yêu cầu tuần 1](docs/00-plan.md)
- [Dịch vụ và yêu cầu](docs/01-services-and-requirements.md)
- [Thiết kế kiến trúc](docs/02-architecture.md)
- [Sơ đồ kiến trúc](diagrams/architecture-week1-simple.png) · [mã Mermaid](diagrams/architecture-week1-simple.mmd)
- [Template CloudFormation](infra/week1-foundation.yaml)
- [Runbook triển khai](docs/03-foundation-runbook.md)
- [Biên bản triển khai](docs/07-deployment-record.md)
- [Rà soát CloudTrail](docs/08-cloudtrail-audit.md)
- [Ảnh AWS Learner Lab](evidence/README.md)
- [Worklog tuần 1](docs/worklog.csv)

## Minh chứng commit

Các mốc dưới đây lấy từ lịch sử Git của nhánh `main`, theo giờ Việt Nam (UTC+07).

| Thời điểm commit | Nội dung | Link commit |
|---|---|---|
| 08/10/2026, 13:02 | Thêm template CloudFormation, tài liệu thiết kế, biên bản và ảnh nền tảng tuần 1. Khi đó tài liệu nằm trong `docs/week-1/`, template nằm trong `infra/`. | [4bb8fd8 — nền tảng tuần 1](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/4bb8fd84ba471d9fd4c3e727f632e8bcd4818dfc) |
| 15/10/2026, 21:57 | Bổ sung file `docs/data-sources.md` để xác định API nguồn, phạm vi dữ liệu và cách diễn giải kết quả. | [c54b76f — thêm tài liệu nguồn dữ liệu](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/c54b76f718fb1f7aa37d9b918047297a1119cd55) |
| 16/10/2026, 08:19 | Chuyển tài liệu, template, sơ đồ, script và ảnh tuần 1 vào thư mục riêng `tuan_1/`; cập nhật các đường dẫn liên quan. | [7d0290b — tách thư mục tuần 1](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/7d0290bccc02b0af9e19141dd439947f764ba8e3) |

Hai commit ngày 15–16/10 là các lần bổ sung tài liệu và tổ chức lại repository sau lần nộp đầu. Ngày triển khai AWS được đối chiếu riêng trong [biên bản ngày 08/10](docs/07-deployment-record.md) và [CloudTrail](docs/08-cloudtrail-audit.md).

Các file để đối chiếu trực tiếp: [báo cáo tuần 1](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_1/README.md), [template nền tảng](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_1/infra/week1-foundation.yaml), [biên bản triển khai](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_1/docs/07-deployment-record.md), [nguồn dữ liệu](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/docs/data-sources.md).

## Phân công và thời lượng tuần 1

| Sinh viên | Phân công | Tổng thời lượng sinh viên cung cấp |
|---|---|---|
| Lê Minh Huy — 24110019 | Tìm hiểu dịch vụ; thiết kế và chỉnh sửa sơ đồ/template; thực hiện, kiểm tra nền tảng VPC/LabRole/S3 và tag; rà soát minh chứng. | 8 giờ |

Tổng 8 giờ là thông tin sinh viên đã cung cấp trong quá trình thực hiện dự án. Chưa có ghi chép để phân bổ số giờ theo từng buổi hoặc từng nhiệm vụ; các ô giờ chi tiết trong [worklog](docs/worklog.csv) vì vậy vẫn để trống. CloudTrail và thời gian phiên Lab không xác nhận tổng giờ học của sinh viên.

LLM/AI (ChatGPT) hỗ trợ tra cứu, soạn tài liệu/sơ đồ và trực tiếp thực thi một số lệnh triển khai, kiểm tra theo [biên bản](docs/07-deployment-record.md). Các thao tác có AI hỗ trợ được ghi riêng trong worklog.

## Kế hoạch tuần 2

Người phụ trách: Lê Minh Huy — 24110019. Triển khai theo thứ tự dưới đây, kiểm thử từng thành phần trước khi nối luồng dữ liệu.

| Thứ tự | Công việc | Kết quả cần kiểm tra |
|---|---|---|
| 1 | Tạo bảng snapshot DynamoDB và Lambda kiểm kê EC2, RDS, SageMaker, EKS ở `us-east-1` và `us-west-2`. | Gọi API thành công, lưu được snapshot theo dịch vụ/Region; phân biệt không có tài nguyên với lỗi hoặc thiếu quyền. |
| 2 | Triển khai Lambda chi phí dùng Cost Explorer và lưu kết quả vào DynamoDB. | Kiểm tra kỳ dữ liệu, tiền tệ, cờ `Estimated` và giới hạn lượt gọi; API đọc dùng snapshot đã lưu. |
| 3 | Tạo Lambda đọc dữ liệu và route `GET /summary` trên API Gateway, có xác thực. | Request được xác thực đọc được dữ liệu; request không có quyền bị từ chối. |
| 4 | Tạo hai lịch EventBridge riêng cho kiểm kê và chi phí. | Kiểm tra lịch, target, quyền gọi Lambda và lần thực thi; Cost Explorer chỉ được gọi vài lần/ngày theo đề bài. |
| 5 | Đưa giao diện lên S3, hiển thị dữ liệu JSON lấy từ API đã xác thực. | Kiểm tra số liệu, thời điểm snapshot và trạng thái lỗi; giữ cấu hình bảo vệ dữ liệu và thông tin đăng nhập. |
| 6 | Triển khai cảnh báo SNS và kiểm thử các thành phần. | Kiểm tra ngưỡng, xác nhận subscription, nhận email thử và lưu kết quả/ảnh minh chứng theo từng chức năng. |

Đây là kế hoạch chuyển tiếp từ tuần 1. Kết quả thực hiện được ghi riêng trong [báo cáo tuần 2](../tuan_2/README.md); thời lượng thực tế của tuần 2 được ghi trong [worklog tuần 2](../tuan_2/worklog.csv).
