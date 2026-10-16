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
- [Phân công, các mốc thời gian và thời lượng tuần 1 — tài liệu riêng](docs/10-week1-assignment-and-time.md)
- [Kế hoạch tuần 2 — tài liệu riêng](docs/09-week2-plan.md)

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

[Mở tài liệu Phân công và thời lượng tuần 1](docs/10-week1-assignment-and-time.md), gồm phân công theo nhóm việc, các mốc AWS ngày 08/10, các mốc chuẩn bị/rà soát và lưu tài liệu ngày 07–10/10, tổng thời lượng 8 giờ do sinh viên cung cấp và phần có LLM/AI (ChatGPT) hỗ trợ. Giờ chi tiết từng nhiệm vụ chưa có ghi chép phân bổ; các mốc API và Git không được dùng để suy ra thời lượng cá nhân.

## Kế hoạch tuần 2

[Mở tài liệu Kế hoạch tuần 2](docs/09-week2-plan.md). Tài liệu trình bày riêng mục tiêu, thứ tự triển khai các dịch vụ lõi, kết quả cần kiểm thử, người phụ trách và cách ghi nhật ký thực hiện.
