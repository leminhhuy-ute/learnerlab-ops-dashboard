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

LLM/AI (ChatGPT) hỗ trợ tra cứu, soạn tài liệu/sơ đồ và trực tiếp thực thi một số lệnh triển khai, kiểm tra theo biên bản. Worklog để trống giờ sinh viên chưa có dữ liệu thời lượng; mốc CloudTrail không được dùng để suy ra giờ học.
